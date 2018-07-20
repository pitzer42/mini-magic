class Resources:

    def __init__(self, **kwargs):
        self.a = 0
        self.b = 0
        expand(Resources, kwargs, obj=self)

    def enough(self, cost):
        for resource_type in self.__dict__:
            owned = self.__getattribute__(resource_type)
            desired = cost.__getattribute__(resource_type)
            if owned < desired:
                return False
        return True

    def consume(self, cost):
        for resource_type in self.__dict__:
            amount = self.__getattribute__(resource_type)
            amount -= cost.__getattribute__(resource_type)
            self.__setattr__(resource_type, amount)

    def empty(self):
        for resource_type in self.__dict__:
            self.__setattr__(resource_type, 0)


class Card:

    def __init__(self, **kwargs):
        self._id = None
        self.name = None
        self.cost = Resources()
        self.attack = 0
        self.defense = 0
        self.tapped = False
        expand(Card, kwargs, obj=self)


class Deck:

    def __init__(self, **kwargs):
        self._id = None
        self.cards = list()
        expand(Deck, kwargs, obj=self)


class Match:

    class ImpossibleOperation(Exception):

        def __init__(self, message):
            super(Match.ImpossibleOperation, self).__init__(message)

    class States:
        waiting_for_players = 'waiting_for_players'
        phase_1 = 'phase_1'

    def __init__(self, **kwargs):
        self._id = None
        self.players = list()
        self.last_draw = None
        self.current_player_index = 0
        self.state = Match.States.waiting_for_players
        expand(Match, kwargs, obj=self)

    def current_player(self):
        return self.players[self.current_player_index]

    def add_player(self, player):
        if self.state != Match.States.waiting_for_players:
            raise Match.ImpossibleOperation('Players cannot join the match after it has already started')
        self.players.append(player)

    def start(self):
        if self.state != Match.States.waiting_for_players:
            raise Match.ImpossibleOperation('A match only starts once')
        elif len(self.players) < 2:
            raise Match.ImpossibleOperation('A match cannot start with less than two players')
        self.state = Match.States.phase_1

    def draw(self):
        if self.state != Match.States.phase_1:
            raise Match.ImpossibleOperation('A player can only draw during in Phase 1')
        if self.last_draw == self.current_player_index:
            raise Match.ImpossibleOperation('A player can only draw once per turn')
        self.current_player().draw()
        self.last_draw = self.current_player_index

    def play_card(self, card_index):
        if self.state != Match.States.phase_1:
            raise Match.ImpossibleOperation('A player can only play a card during in Phase 1')
        card = self.current_player().hand.pop(card_index)
        if not self.current_player().resources.enough(card.cost):
            raise Match.ImpossibleOperation('The current player does not have enough resources to play this card')
        self.current_player().resources.consume(card.cost)
        self.current_player().field.append(card)

    def end_turn(self):
        if self.state != Match.States.phase_1:
            raise Match.ImpossibleOperation('Turn can only end after Phase 1')
        if self.current_player_index + 1 == len(self.players):
            self.current_player_index = 0
        else:
            self.current_player_index += 1
        self.state = Match.States.phase_1
        for player in self.players:
            player.resources.empty()


class Player:

    def __init__(self, **kwargs):
        self._id = None
        self.hand = list()
        self.deck = list()
        self.field = list()
        self.discard = list()
        self.resources = Resources()
        expand(Player, kwargs, obj=self)

    def draw(self):
        top_card = self.deck.pop()
        self.hand.append(top_card)


NESTED_ATTRIBUTES_MAP = {
    'Card.cost': Resources,
    'Player.resources': Resources,
    'Player.hand': [Card, ],
    'Match.players': [Player, ],
}


def expand(cls, flat_dict, obj=None):
    if obj is None:
        obj = cls()
    if type(flat_dict) is not dict:
        flat_dict = flat_dict.__dict__
    for key in flat_dict:
        if hasattr(obj, key):
            value = flat_dict[key]
            attribute_name = cls.__name__ + '.' + key
            if attribute_name in NESTED_ATTRIBUTES_MAP:
                nested_cls = NESTED_ATTRIBUTES_MAP[attribute_name]
                if type(nested_cls) is list:
                    value = [expand(nested_cls[0], item) for item in value]
                else:
                    value = expand(nested_cls, value)
            setattr(obj, key, value)
    return obj


def expand_many(cls, flat_dict_list):
    return [expand(cls, flat_dict) for flat_dict in flat_dict_list]


def flatten(obj):
    cls_name = type(obj).__name__
    flat_dict = dict(obj.__dict__)
    for key in flat_dict:
        attribute_name = cls_name + '.' + key
        if attribute_name in NESTED_ATTRIBUTES_MAP:
            nested_cls = NESTED_ATTRIBUTES_MAP[attribute_name]
            if type(nested_cls) is list:
                flat_dict[key] = [flatten(item) for item in flat_dict[key]]
            else:
                flat_dict[key] = flatten(flat_dict[key])
    return flat_dict



