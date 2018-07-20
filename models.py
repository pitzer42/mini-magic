import storage


class IllegalOperation(Exception):

    def __init__(self, message):
        super(IllegalOperation, self).__init__(message)


class MatchStates:
    waiting_for_players = 'waiting_for_players'
    phase_1 = 'phase_1'


def create_resources(**kwargs):
    obj = dict()
    obj['a'] = 0
    obj['b'] = 0
    obj.update(kwargs)
    return obj


def create_card(**kwargs):
    obj = dict()
    obj['_id'] = None
    obj['name'] = None
    obj['cost'] = create_resources()
    obj['attack'] = 0
    obj['defense'] = 0
    obj['activated'] = False
    obj.update(kwargs)
    return obj


def create_deck(**kwargs):
    obj = dict()
    obj['_id'] = None
    obj['card_ids'] = list()
    obj.update(kwargs)
    return obj


def create_match(*args, **kwargs):
    if len(args) > 0:
        kwargs = dict(args[0])
    obj = dict()
    obj['_id'] = None
    obj['players'] = list()
    obj['last_draw'] = None
    obj['current_player_index'] = 0
    obj['state'] = MatchStates.waiting_for_players
    obj.update(kwargs)
    return obj


def create_player(**kwargs):
    obj = dict()
    obj['_id'] = None
    obj['hand'] = list()
    obj['field'] = list()
    obj['deck'] = list()
    obj['discard'] = list()
    obj['health_points'] = 20
    obj['resources'] = create_resources()
    obj.update(kwargs)
    return obj


def add_player_to_match(match, player, deck):
    if match['state'] != MatchStates.waiting_for_players:
        raise IllegalOperation('Players cannot join the match after it has already started')
    player['health_points'] = 20
    player['deck'] = deck['card_ids']
    if match['players'] is None:
        match['players'] = list()
    match['players'].append(player)
    storage.update_match(match)
    return match


def start_match(match):
    if match['state'] != MatchStates.waiting_for_players:
        raise IllegalOperation('A match only starts once')
    elif len(match['players']) < 2:
        raise IllegalOperation('A match cannot start with less than two players')
    match['state'] = MatchStates.phase_1


def change_turn(match):
    if match['state'] != MatchStates.phase_1:
        raise IllegalOperation('A match must start before change turns')
    for player in match['players']:
        empty_resources(player['resources'])
    match['state'] = MatchStates.phase_1
    if match['current_player_index'] + 1 < len(match['players']):
        match['current_player_index'] += 1
    else:
        match['current_player_index'] = 0
    return match


def empty_resources(resources):
    for resource_type in resources:
        resources[resource_type] = 0


def draw(match):
    if match['state'] != MatchStates.phase_1:
        raise IllegalOperation('A match must start before a player draw')
    index = match['current_player_index']
    player = match['players'][index]
    card_id = player['deck'].pop()
    card = storage.get_card(card_id)
    player['hand'].append(card)


def play_card(match, player_index, card_index):
    if match['state'] != MatchStates.phase_1:
        raise IllegalOperation('A match must start before a play')
    player = match['players'][player_index]
    card = player['hand'][card_index]
    if not_enough_resources(player['resources'], card['cost']):
        raise IllegalOperation('Player does not have enough resources to play this card')
    player['hand'].pop(card_index)
    consume(player['resources'], card['cost'])
    if player['field'] is None:
        player['field'] = list()
    player['field'].append(card)


def not_enough_resources(have, want):
    for resource_type in want:
        if want[resource_type] > have[resource_type]:
            return True
    return False


def consume(have, want):
    for resource_type in want:
        have[resource_type] -= want[resource_type]


def current_player(match):
    return match['players'][match['current_player_index']]
