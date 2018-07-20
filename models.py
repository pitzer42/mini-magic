class Resources:

    def __init__(self, **kwargs):
        self.a = 0
        self.b = 0
        expand(self, kwargs)

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

    @classmethod
    def create_many(cls, dict_list):
        return [Card.create(flat_dict) for flat_dict in dict_list]

    @classmethod
    def create(cls, flat_dict):
        card = Card()
        expand(card, flat_dict)
        return card

    def __init__(self, **kwargs):
        self._id = None
        self.name = None
        self.cost = Resources()
        self.attack = 0
        self.defense = 0
        self.tapped = False
        expand(self, kwargs)


class Deck:

    @classmethod
    def create_many(cls, dict_list):
        return [Deck.create(flat_dict) for flat_dict in dict_list]

    @classmethod
    def create(cls, flat_dict):
        deck = Deck()
        expand(deck, flat_dict)
        return deck

    def __init__(self, **kwargs):
        self._id = None
        self.cards = list()
        expand(self, kwargs)


class Match:

    class ImpossibleOperation(Exception):

        def __init__(self, message):
            super(Match.ImpossibleOperation, self).__init__(message)

    class States:
        waiting_for_players = 'waiting_for_players'
        phase_1 = 'phase_1'

    @classmethod
    def create_many(cls, dict_list):
        return [Match.create(flat_dict) for flat_dict in dict_list]

    @classmethod
    def create(cls, flat_dict):
        match = Match()
        expand(match, flat_dict)
        return match

    def __init__(self, **kwargs):
        self._id = None
        self.players = list()
        self.last_draw = None
        self.current_player_index = 0
        self.state = Match.States.waiting_for_players
        expand(self, kwargs)

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

    @classmethod
    def create_many(cls, dict_list):
        return [Player.create(flat_dict) for flat_dict in dict_list]

    @classmethod
    def create(cls, flat_dict):
        player = Player()
        expand(player, flat_dict)
        return player

    def __init__(self, **kwargs):
        self._id = None
        self.hand = list()
        self.deck = list()
        self.field = list()
        self.discard = list()
        self.resources = Resources()
        expand(self, kwargs)

    def draw(self):
        top_card = self.deck.pop()
        self.hand.append(top_card)


"""
Think in something better.
Remove nesting_map
Remove static builders from classes
"""


NESTTING_MAP = {
    'cost': Resources,
    'resources': Resources,
    'players': [Player, ]
}


def expand(obj, flat_dict):
    if type(flat_dict) is not dict:
        return
    for key in flat_dict:
        if hasattr(obj, key):
            if key in NESTTING_MAP.keys():
                if type(NESTTING_MAP[key]) is list:
                    list_attribute = list()
                    for item in flat_dict[key]:
                        nested_obj = NESTTING_MAP[key][0]()
                        expand(nested_obj, item)
                        list_attribute.append(nested_obj)
                    setattr(obj, key, list_attribute)
                else:
                    nested_obj = NESTTING_MAP[key]()
                    expand(nested_obj, flat_dict[key])
                    setattr(obj, key, nested_obj)
            else:
                setattr(obj, key, flat_dict[key])


def flatten(obj):
    if not hasattr(obj, '__dict__'):
        return obj
    flat = dict(obj.__dict__)
    for key in flat:
        if key in NESTTING_MAP.keys():
            if type(NESTTING_MAP[key]) is list:
                list_attribute = list()
                for item in flat[key]:
                    list_attribute.append(flatten(item))
                flat[key] = list_attribute
            else:
                flat[key] = flatten(flat[key])
    return flat
