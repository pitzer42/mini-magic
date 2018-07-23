import events
import effects
from functools import wraps
from entities import Deck, Player, Match, GameOverException


class IllegalOperation(Exception):

    def __init__(self, message):
        super(IllegalOperation, self).__init__(message)


def legal(*legal_events):
    def decorator(f):
        def wrapped_f(*args, **kwargs):
            match = Match.get(args[0])
            last_event_name = match.log[-1]['name']
            if last_event_name not in legal_events:
                raise IllegalOperation('This operation is not allowed during ' + last_event_name)
            f(*args, **kwargs)
        return wrapped_f
    return decorator


def legal_for_prompted(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        match = Match.get(args[0])
        last_event = match.log[-1]
        if last_event['name'] != events.Prompt:
            raise IllegalOperation('You were not prompted')
        player_index = args[1]
        player_id = match.players[player_index]._id
        prompted_id = last_event['args'][0]
        if player_id != prompted_id:
            raise IllegalOperation('You were not prompted')
        return f(*args, **kwargs)
    return wrapped


def expect_game_over(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except GameOverException as e:
            log = Match.get(args[0]).log
            events.publish(log, events.GameOver, e.winner)
    return wrapped


@legal(events.Setup)
@expect_game_over
def join(match_id, player_id, deck_id):
    match = Match.get(match_id)
    if match is None:
        raise IllegalOperation('Match ' + match_id + ' not found')
    if match.get_player_by_id(player_id):
        raise IllegalOperation('This player have already joined to this match')
    player = Player.get(player_id)
    if player is None:
        raise IllegalOperation('Player ' + player_id + ' not found')
    deck = Deck.get(deck_id)
    if deck is None:
        raise IllegalOperation('Deck ' + deck_id + ' not found')
    events.publish(match.log, events.PlayerJoin, player_id)
    player.deck = deck
    match.players.append(player)
    if match.has_enough_players():
        events.publish(match.log, events.Ready)
        for p in match.players:
            events.publish(match.log, events.InitialDraw, p._id)
            for i in range(0,Match.INITIAL_HAND_SIZE):
                card = p.deck.top()
                p.hand.append(card)
        current_player = match.current_player()
        events.publish(match.log, events.TurnBegin, current_player._id)

        events.publish(match.log, events.Refresh, current_player._id)
        for card in current_player.board:
            card.activated = False
        events.publish(match.log, events.Draw, current_player._id)
        card = current_player.deck.top()
        current_player.hand.append(card)
        events.publish(match.log, events.Prompt, current_player._id)

    else:
        events.publish(match.log, events.Setup)
    match.save()


@legal_for_prompted
def play_card(match_id, player_index, card_index):
    match = Match.get(match_id)
    if match is None:
        raise IllegalOperation('Match ' + match_id + ' not found')
    if player_index < 0 or player_index >= len(match.players):
        raise IllegalOperation('Player at ' + player_index + ' not found')
    player = match.players[player_index]
    if card_index < 0 or card_index >= len(player.hand):
        raise IllegalOperation('Card at ' + card_index + ' not found')
    card = player.hand[card_index]
    if not player.resources.enough(card.cost):
        raise IllegalOperation('Player does not have enough resources to play ' + card._id)
    events.publish(match.log, events.Play, player._id, card._id)
    player.hand.pop(card_index)
    player.resources.consume(card.cost)
    player.board.append(card)
    events.publish(match.log, events.Prompt, match.next_player()._id)
    match.save()


@legal_for_prompted
@expect_game_over
def use_card(match_id, player_index, card_index):
    match = Match.get(match_id)
    if match is None:
        raise IllegalOperation('Match ' + match_id + ' not found')
    if player_index < 0 or player_index >= len(match.players):
        raise IllegalOperation('Player at ' + str(player_index) + ' not found')
    player = match.players[player_index]
    if card_index < 0 or card_index >= len(player.board):
        raise IllegalOperation('Card at ' + str(card_index) + ' not found')
    card = player.board[card_index]
    if card.activated:
        raise IllegalOperation('This card was already been during this turn')
    events.publish(match.log, events.Use, player._id, card._id)
    card.activated = True
    if card.effect_id:
        effects.apply(match, player, card, card.effect_id)
    events.publish(match.log, events.Prompt, match.next_player(current=player)._id)
    match.save()


@legal_for_prompted
def yield_play(match_id, player_index):
    match = Match.get(match_id)
    if match is None:
        raise IllegalOperation('Match ' + match_id + ' not found')
    if player_index < 0 or player_index >= len(match.players):
        raise IllegalOperation('Player at ' + player_index + ' not found')
    player = match.players[player_index]
    events.publish(match.log, events.Yield, player._id)
    next_player = match.next_player(current=player)
    events.publish(match.log, events.Prompt, next_player._id)
    match.save()


@legal_for_prompted
def end_turn(match_id, player_index):
    match = Match.get(match_id)
    if match is None:
        raise IllegalOperation('Match ' + match_id + ' not found')
    if player_index < 0 or player_index >= len(match.players):
        raise IllegalOperation('Player at ' + player_index + ' not found')
    player = match.players[player_index]
    events.publish(match.log, events.TurnEnd, player._id)
    player.resources.empty()
    if match.current_player_index + 1 == len(match.players):
        match.current_player_index = 0
    else:
        match.current_player_index += 1
    begin_turn(match, match.current_player())
    match.save()


def begin_turn(match, current_player):
    events.publish(match.log, events.TurnBegin, current_player._id)
    events.publish(match.log, events.Refresh, current_player._id)
    for card in current_player.board:
        card.activated = False
    events.publish(match.log, events.Draw, current_player._id)
    card = current_player.deck.top()
    current_player.hand.append(card)
    events.publish(match.log, events.Prompt, current_player._id)
