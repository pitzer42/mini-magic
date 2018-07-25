import events
import effects
from functools import wraps
from entities import Deck, Player, Match, GameOverException


class IllegalOperation(Exception):

    def __init__(self, message):
        super(IllegalOperation, self).__init__(message)


def assert_get_resource_by_index(index, container, entity_name):
    if index < 0 or index >= len(container):
        raise IllegalOperation(entity_name + ' ' + index + ' not found')
    return container[index]


def assert_get_resource_by_id(resource_id, container):
    resource = container.get(resource_id)
    if resource is None:
        raise IllegalOperation(container.__name__ + ' ' + resource_id + ' not found')
    return resource


def user_action(*legal_events):
    def decorator(f):
        def wrapped(*args, **kwargs):
            match = assert_get_resource_by_id(args[0], Match)
            event = match.last_event
            if event['name'] not in legal_events:
                raise IllegalOperation('This operation is not allowed during ' + event['name'])
            if event['name'] == events.Prompt:
                prompted_id = event['args'][0]
                player_id = match.players[args[1]].id
                if prompted_id != player_id:
                    raise IllegalOperation('You were not prompted')
            args = (match, ) + args[1:]
            try:
                return f(*args, **kwargs)
            except GameOverException as e:
                match.publish(events.GameOver, e.winner)
            finally:
                match.save()
        return wrapped
    return decorator


@user_action(events.Setup)
def join(match, player_id, deck_id):
    if match.get_player_by_id(player_id):
        raise IllegalOperation('This player have already joined to this match')
    player = assert_get_resource_by_id(player_id, Player)
    deck = assert_get_resource_by_id(deck_id, Deck)
    events.publish(match.log, events.PlayerJoin, player_id)
    on_player_join(match, player, deck)


def on_player_join(match, player, deck):
    player.deck = deck
    match.players.append(player)
    if match.has_enough_players():
        events.publish(match.log, events.Ready)
        on_ready(match)
    else:
        events.publish(match.log, events.Setup)


def on_ready(match):
    for player in match.players:
        events.publish(match.log, events.InitialDraw, player.id)
        on_initial_hand_size(player)
    current_player = match.current_player()
    events.publish(match.log, events.TurnBegin, current_player.id)
    begin_turn(match, current_player)


def on_initial_hand_size(player):
    for i in range(0, Match.INITIAL_HAND_SIZE):
        card = player.deck.top()
        player.hand.append(card)


def begin_turn(match, current_player):
    events.publish(match.log, events.Refresh, current_player.id)
    on_refresh(current_player)
    events.publish(match.log, events.Draw, current_player.id)
    on_draw(current_player)
    events.publish(match.log, events.Prompt, current_player.id)


def on_refresh(player):
    for card in player.board:
        card.activated = False


def on_draw(player):
    card = player.deck.top()
    player.hand.append(card)


@user_action(events.Prompt)
def play_card(match, player_index, card_index):
    player = assert_get_resource_by_index(player_index, match.players, 'Player')
    card = assert_get_resource_by_index(card_index, player.hand, 'Card')
    if not player.resources.enough(card.cost):
        raise IllegalOperation('Player does not have enough resources to play ' + card.id)
    events.publish(match.log, events.Play, player.id, card.id)
    on_play(player, card_index, card)
    events.publish(match.log, events.Prompt, match.next_player().id)


def on_play(player, card_index, card):
    player.hand.pop(card_index)
    player.resources.consume(card.cost)
    player.board.append(card)


@user_action(events.Prompt)
def use_card(match, player_index, card_index):
    player = assert_get_resource_by_index(player_index, match.players, 'Player')
    card = assert_get_resource_by_index(card_index, player.board, 'Card')
    if card.activated:
        raise IllegalOperation('This card was already been during this turn')
    events.publish(match.log, events.Use, player.id, card.id)
    on_use_card(match, player, card)
    events.publish(match.log, events.Prompt, match.next_player(current=player).id)


def on_use_card(match, player, card):
    card.activated = True
    if card.effect_id:
        effects.apply(match, player, card, card.effect_id)


@user_action(events.Prompt)
def yield_play(match, player_index):
    player = assert_get_resource_by_index(player_index, match.players, 'Player')
    events.publish(match.log, events.Yield, player.id)
    on_yield(match, player)


def on_yield(match, player):
    next_player = match.next_player(current=player)
    events.publish(match.log, events.Prompt, next_player.id)


@user_action(events.Prompt)
def end_turn(match, player_index):
    player = assert_get_resource_by_index(player_index, match.players, 'Player')
    events.publish(match.log, events.TurnEnd, player.id)
    on_turn_end(match, player)


def on_turn_end(match, player):
    player.resources.empty()
    if match.current_player_index + 1 == len(match.players):
        match.current_player_index = 0
    else:
        match.current_player_index += 1
    begin_turn(match, match.current_player())



