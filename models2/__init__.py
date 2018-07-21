import models2.events as events

class AttrDict:

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            kwargs.update(dict(args[0]))
        self.from_dict(kwargs)

    def from_dict(self, data_dict):
        for key in data_dict:
            value = data_dict[key]
            if type(value) is dict:
                value = AttrDict(value)
            self.__dict__[key] = value

    def to_dict(self):
        data_dict = dict(self.__dict__)
        for key in data_dict:
            value = data_dict[key]
            if type(value) is AttrDict:
                data_dict[key] = value.to_dict()
        return data_dict


class Resources(AttrDict):

    def __init__(self, *args, **kwargs):
        self.a = 0
        self.b = 0
        super(Resources, self).__init__(*args, **kwargs)


class Card(AttrDict):

    def __init__(self, *args, **kwargs):
        self.name = None
        self.cost = Resources()
        self.attack = 0
        self.defense = 0
        self.activated = False
        self.effect_id = None
        super(Card, self).__init__(*args, **kwargs)


class Deck(AttrDict):

    def __init__(self, *args, **kwargs):
        self.card_ids = list()
        super(Deck, self).__init__(*args, **kwargs)


class Player(AttrDict):

    INITIAL_HP = 20

    def __init__(self, *args, **kwargs):
        self.hand = list()
        self.board = list()
        self.deck = list()
        self.discard = list()
        self.hp = Player.INITIAL_HP
        self.resources = Resources()
        super(Player, self).__init__(*args, **kwargs)


class Match(AttrDict):

    MIN_PLAYER = 2

    def __init__(self, *args, **kwargs):
        self.log = [events.SETUP_EVENT]
        self.players = list()
        self.current_player_index = 0
        super(Match, self).__init__(*args, **kwargs)

    def current_player(self):
        return self.players[self.current_player_index]

    def has_enough_players(self):
        return len(self.players) >= Match.MIN_PLAYER

    def get_player(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player
        return None













