import models2.events as events
import models2.storage as storage


class AttrDict:

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            kwargs.update(dict(args[0]))
        self.__dict__.update(kwargs)

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

    @classmethod
    def get(cls, card_id):
        return storage.get_card(card_id)

    def __init__(self, *args, **kwargs):
        self.name = None
        self.cost = None
        self.attack = 0
        self.defense = 0
        self.activated = False
        self.effect_id = None
        super(Card, self).__init__(*args, **kwargs)
        self.cost = Resources() if self.cost is None else Resources(self.cost)


class Deck(AttrDict):

    def __init__(self, *args, **kwargs):
        self.card_ids = list()
        super(Deck, self).__init__(*args, **kwargs)

    def top(self):
        return Card.get(self.card_ids.pop())


class Player(AttrDict):

    INITIAL_HP = 20

    def __init__(self, *args, **kwargs):
        self.hand = list()
        self.board = list()
        self.deck = None
        self.discard = list()
        self.hp = Player.INITIAL_HP
        self.resources = None
        super(Player, self).__init__(*args, **kwargs)
        self.resources = Resources() if self.resources is None else Resources(self.resources)
        self.deck = Deck() if self.deck is None else Deck(self.deck)

    def draw(self, amount):
        for i in range(0, amount):
            try:
                top_card = self.deck.top()
                self.hand.append(top_card)
            except IndexError:
                raise GameOverException


class Match(AttrDict):

    MIN_PLAYER = 2

    def __init__(self, *args, **kwargs):
        self.log = [events.SETUP_EVENT]
        self.players = list()
        self.current_player_index = 0
        super(Match, self).__init__(*args, **kwargs)
        players = list()
        if len(self.players) > 0:
            for data in self.players:
                players.append(Player(data))
            self.players = players

    def current_player(self):
        return self.players[self.current_player_index]

    def has_enough_players(self):
        return len(self.players) >= Match.MIN_PLAYER

    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def join(self, player, deck):
        player.deck = deck
        self.players.append(player)
        events.publish(self.log, events.PlayerJoin, player._id)


class GameOverException(Exception):
    pass
