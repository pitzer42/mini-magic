import storage
from log_list import LogListener, publish

MIN_PLAYERS_PER_MATCH = 2
INITIAL_HAND_SIZE = 7


def resources(*args, **kwargs):
    if len(args) > 0:
        kwargs = dict(args[0])
    obj = dict()
    obj['a'] = 0
    obj['b'] = 0
    obj.update(kwargs)
    return obj


def card(*args, **kwargs):
    if len(args) > 0:
        kwargs = dict(args[0])
    obj = dict()
    obj['_id'] = None
    obj['name'] = None
    obj['cost'] = resources()
    obj['attack'] = 0
    obj['defense'] = 0
    obj['activated'] = False
    obj['effect_id'] = None
    obj.update(kwargs)
    return obj


def deck(*args, **kwargs):
    if len(args) > 0:
        kwargs = dict(args[0])
    obj = dict()
    obj['_id'] = None
    obj['card_ids'] = list()
    obj.update(kwargs)
    return obj


def player(*args, **kwargs):
    if len(args) > 0:
        kwargs = dict(args[0])
    obj = dict()
    obj['_id'] = None
    obj['hand'] = list()
    obj['board'] = list()
    obj['deck'] = list()
    obj['discard'] = list()
    obj['health_points'] = 20
    obj['resources'] = resources()
    obj.update(kwargs)
    return obj


def match(*args, **kwargs):
    if len(args) > 0:
        kwargs = dict(args[0])
    obj = dict()
    obj['_id'] = None
    obj['log'] = list()
    obj['players'] = list()
    obj['last_draw'] = None
    obj['current_player_index'] = 0
    obj.update(kwargs)
        publish(obj['log'], Events.Setup)
    return obj


def has_enough_players(_match):
    return len(_match['players']) >= MIN_PLAYERS_PER_MATCH


def find_player_by_id(_match, _id):
    for _player in _match['players']:
        if _player['_id'] == _id:
            return _player


def current_player(_match):
    index = _match['current_player_index']
    return _match['players'][index]


class Events:
    Setup = 'setup'
    PlayerJoin = 'player_join'
    Ready = 'ready'
    InitialDraw = 'initial_draw'
    TurnBegin = 'turn_begin'
    Refresh = 'refresh'
    Draw = 'draw'
    Prompt = 'prompt'
    TurnEnd = 'turn_end'
    GameOver = 'game_over'
    Play = 'play'
    Use = 'use'
    Activate = 'activate'
    Yield = 'yield'


class GameOverException(Exception):
    pass


class MiniMagicEngine(LogListener):

    def __init__(self, *args):
        super(MiniMagicEngine, self).__init__()
        if len(args) != 1:
            raise Exception('a dict was expected as parameter')
        self.match = args[0]
        self.connect('log', self.match)

    def _on_player_join(self, player_id):
        if has_enough_players(self.match):
            self.publish(Events.Ready)
        else:
            self.publish(Events.Setup)

    def _on_ready(self):
        self.publish(Events.InitialDraw)
        self.publish(Events.TurnBegin, current_player(self.match)['_id'])
        self.publish(Events.Refresh)

    def _on_initial_draw(self):
        for _player in self.match['players']:
            draw(self.match, _player['_id'], INITIAL_HAND_SIZE)

    def _on_refresh(self):
        _player = current_player(self.match)
        for _card in _player['board']:
            _card['activated'] = False
        self.publish(Events.Draw, _player['_id'])

    def _on_draw(self, player_id):
        draw(self.match, player_id, 1)
        self.publish(Events.Prompt, player_id)

    def _on_yield(self, player_id):
        pass



class IllegalOperation(Exception):

    def __init__(self, message):
        super(IllegalOperation, self).__init__(message)


def legal(*events):
    def decorator(f):
        def wrapped_f(*args, **kwargs):
            _match = args[0]
            last_event = _match['log'][-1]['name']
            if last_event not in events:
                raise IllegalOperation('This operation is not allowed during ' + last_event)
            f(*args, **kwargs)
        return wrapped_f
    return decorator


@legal(Events.Setup)
def add_player_to_match(_match, _player, _deck):
    _player['deck'] = _deck['card_ids']
    _match['players'].append(_player)
    publish(_match['log'], Events.PlayerJoin, _player['_id'])


@legal(Events.InitialDraw, Events.Draw)
def draw(_match, player_id, amount):
    _player = find_player_by_id(_match, player_id)
    _deck = _player['deck']
    _hand = _player['hand']
    for i in range(0, amount):
        try:
            card_id = _deck.pop()
        except IndexError:
            raise GameOverException()
        _card = storage.get_card(card_id)
        _hand.append(_card)


def is_not_being_prompted(_match, _player):
    last_event = _match['log'][-1]
    prompted_id = last_event['args'][0]
    return _player['_id'] != prompted_id


@legal(Events.Prompt, Events.Play, Events.Use)
def play_card(_match, player_index, card_index):
    _player = _match['players'][player_index]
    if is_not_being_prompted(_match, _player):
        raise IllegalOperation('Waiting for other player')
    _card = _player['hand'][card_index]
    if not_enough_resources(_player['resources'], _card['cost']):
        raise IllegalOperation('Player does not have enough resources to play this card')
    _player['hand'].pop(card_index)
    consume(_player['resources'], _card['cost'])
    _player['board'].append(_card)
    publish(_match['log'], Events.Play, _player['_id'], _card['_id'])


@legal(Events.Prompt, Events.Play, Events.Use)
def use_card(_match, player_index, card_index):
    _player = _match['players'][player_index]
    if is_not_being_prompted(_match, _player):
        raise IllegalOperation('Waiting for other player')
    _card = _player['board'][card_index]
    _card['activated'] = True
    effect_id = _card['effect_id']
    if effect_id is not None:
        publish(_match['log'], Events.Use, _player['_id'], _card['_id'])
        apply_effect(_match, _player, _card, effect_id)


@legal(Events.Prompt, Events.Play, Events.Use)
def yield_play(_match, player_index):
    _player = _match['players'][player_index]
    if is_not_being_prompted(_match, _player):
        raise IllegalOperation('Waiting for other player')
    publish(_match['log'], Events.Yield, _player['_id'])

"""
def end_turn(match):
    if match['state'] != Events.phase_1:
        raise IllegalOperation('A match must start before change turns')
    for player in match['players']:
        empty_resources(player['resources'])
    match['state'] = Events.phase_1
    if match['current_player_index'] + 1 < len(match['players']):
        match['current_player_index'] += 1
    else:
        match['current_player_index'] = 0
    for card in current_player(match)['board']:
        card['activated'] = False
    return match
"""


def empty_resources(resources):
    for resource_type in resources:
        resources[resource_type] = 0


def not_enough_resources(have, want):
    for resource_type in want:
        if want[resource_type] > have[resource_type]:
            return True
    return False


def consume(have, want):
    for resource_type in want:
        have[resource_type] -= want[resource_type]





def apply_effect(match, owner, card, effect_id):
    {
        'add_a': add_a,
        'add_b': add_b,
        '1_damage': one_damage
    }[effect_id](match, owner, card)


def add_a(match, owner, card):
    owner['resources']['a'] += 1


def add_b(match, owner, card):
    owner['resources']['b'] += 1


def one_damage(match, owner, card):
    for player in match['players']:
        if player['_id'] != owner['_id']:
            player['health_points'] -= 1
            return
