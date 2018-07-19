from bson import json_util
import json


class Model:

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            self.from_dict(dictionary)
        self.from_dict(kwargs)

    def to_json(self):
        return json_util.dumps(self.__dict__)

    def from_json(self, string):
        dictionary = json.loads(string)
        self.from_dict(dictionary)

    def from_dict(self, dictionary):
        for key in dictionary:
            if key in self.__dict__:
                setattr(self, key, dictionary[key])


class Card(Model):

    def __init__(self, *initial_data, **kwargs):
        self.id = 0
        self.name = None
        self.cost = dict()
        self.attack = 0
        self.defense = 0
        self.tapped = False
        super(Card, self).__init__(initial_data, kwargs)


class Match(Model):

    class ImpossibleOperation(Exception):

        def __init__(self, message):
            super(Match.ImpossibleOperation, self).__init__(message)

    class States:
        waiting_for_players = 'waiting_for_players',
        phase_1 = 'phase_1',

    def __init__(self, *initial_data, **kwargs):
        self.id = 0
        self.players = list()
        self.last_draw = None
        self.current_player_index = 0
        self.state = Match.States.waiting_for_players
        super(Match, self).__init__(initial_data, kwargs)

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
        if not self.current_player().resources.are_enough(card.cost):
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


class Player(Model):

    def __init__(self, *initial_data, **kwargs):
        self.id = 0
        self.hand = list()
        self.deck = list()
        self.field = list()
        self.discard = list()
        self.resources = Resources()
        super(Player, self).__init__(initial_data, kwargs)

    def draw(self):
        top_card = self.deck.pop()
        self.hand.append(top_card)


class Resources(Model):

    def __init__(self, *initial_data, **kwargs):
        self.a = 0
        self.b = 0
        super(Resources, self).__init__(initial_data, kwargs)

    def are_enough(self, cost):
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

