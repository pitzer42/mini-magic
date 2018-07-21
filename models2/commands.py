import models2.events as events
from models2 import Card, GameOverException


class IllegalOperation(Exception):

    def __init__(self, message):
        super(IllegalOperation, self).__init__(message)


def legal(*legal_events):
    def decorator(f):
        def wrapped_f(*args, **kwargs):
            _match = args[0]
            last_event = _match['log'][-1]['name']
            if last_event not in legal_events:
                raise IllegalOperation('This operation is not allowed during ' + last_event)
            f(*args, **kwargs)
        return wrapped_f
    return decorator


@legal(events.Setup)
def add_player_to_match(match, player, deck):
    player.deck = deck.card_ids
    match.players.append(player)
    events.publish(match.log, events.PlayerJoin, player._id)


@legal(events.InitialDraw, events.Draw)
def draw(match, player_id, amount):
    player = match.get_player(player_id)
    for i in range(0, amount):
        try:
            card_id = player.deck.pop()
        except IndexError:
            raise GameOverException()
        card = Card.get(card_id)
        player.hand.append(card)


@legal(events.Prompt)
def play_card(match, player_index, card_index):
    player = match.players[player_index]
    card = player.hand[card_index]
    if not player.resources.enough(card.cost):
        raise IllegalOperation('Player does not have enough resources to play this card')
    player.hand.pop(card_index)
    player.resources.consume(card.cost)
    player.board.append(card)


@legal(events.Prompt)
def use_card(match, player_index, card_index):
    player = match.players[player_index]
    card = player.board[card_index]
    if card.activated:
        raise IllegalOperation('This card have already been used during this turn')

    player.hand.pop(card_index)
    player.resources.consume(card.cost)
    player.board.append(card)