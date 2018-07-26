import events
import storage
import effects


class ValueObject:

    def __init__(self, *args, **kwargs):
        if len(args) > 0 and args[0] is not None:
            data_dict = args[0]
            if hasattr(data_dict, 'to_dict'):
                data_dict = data_dict.to_dict()
            kwargs.update(data_dict)
        self.__dict__.update(kwargs)

    def to_dict(self):
        data_dict = dict(self.__dict__)
        for key in data_dict:
            value = data_dict[key]
            if hasattr(value, 'to_dict'):
                data_dict[key] = value.to_dict()
            elif type(value) is list:
                list_value = list()
                for item in value:
                    if hasattr(item, 'to_dict'):
                        item = item.to_dict()
                    list_value.append(item)
                data_dict[key] = list_value
        return data_dict


class Resources(ValueObject):

    def __init__(self, *args, **kwargs):
        self.a = 0
        self.b = 0
        super(Resources, self).__init__(*args, **kwargs)

    def enough(self, cost):
        for resource_type in cost.__dict__:
            if not hasattr(self, resource_type):
                return False
            want = getattr(cost, resource_type)
            have = getattr(self, resource_type)
            if want > have:
                return False
        return True

    def consume(self, cost):
        for resource_type in cost.__dict__:
            want = getattr(cost, resource_type)
            have = getattr(self, resource_type)
            setattr(self, resource_type, have - want)

    def empty(self):
        for resource_type in self.__dict__:
            setattr(self, resource_type, 0)


class Entity(ValueObject):

    def __init__(self, *args, **kwargs):
        self._id = None
        super(Entity, self).__init__(*args, **kwargs)

    @classmethod
    def all(cls):
        return [cls(i) for i in storage.all_docs(cls.STORAGE_NAME)]

    @classmethod
    def get(cls, item_id):
        return cls(storage.get_doc(cls.STORAGE_NAME, item_id))

    def save(self):
        self.id = storage.save_doc(self.__class__.STORAGE_NAME, self.to_dict())

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = str(value)


class Card(Entity):

    STORAGE_NAME = 'Cards'

    def __init__(self, *args, **kwargs):
        self.name = None
        self.cost = None
        self.attack = 0
        self.defense = 0
        self.activated = False
        self.effect_id = None
        self.cost = None
        super(Card, self).__init__(*args, **kwargs)
        self.cost = Resources(self.cost)


class Deck(Entity):

    STORAGE_NAME = 'Decks'

    def __init__(self, *args, **kwargs):
        self.card_ids = list()
        super(Deck, self).__init__(*args, **kwargs)

    def top(self):
        card_id = self.card_ids.pop()
        return Card.get(card_id)


class Player(Entity):

    STORAGE_NAME = 'Players'

    INITIAL_HP = 20

    def __init__(self, *args, **kwargs):
        self.hp = Player.INITIAL_HP
        self.hand = list()
        self.board = list()
        self.discard = list()
        self.deck = None
        self.resources = None
        super(Player, self).__init__(*args, **kwargs)
        self.resources = Resources(self.resources)
        self.deck = Deck(self.deck)
        self.hand = [Card(i) for i in self.hand]
        self.board = [Card(i) for i in self.board]
        self.discard = [Card(i) for i in self.discard]


class Match(Entity):

    STORAGE_NAME = 'Matches'

    MIN_PLAYER = 2
    INITIAL_HAND_SIZE = 7

    def __init__(self, *args, **kwargs):
        self.log = [events.SETUP_EVENT]
        self.stack = list()
        self.players = list()
        self.current_player_index = 0
        super(Match, self).__init__(*args, **kwargs)
        players = list()
        for data in self.players:
            players.append(Player(data))
        self.players = players
        stack = list()
        for data in self.stack:
            stack.append(Effect(data))
        self.stack = stack

    def current_player(self):
        return self.players[self.current_player_index]

    def next_player(self, current=None):
        if current is None or current.id == self.current_player().id:
            return self.players[1 - self.current_player_index]
        return self.current_player()

    def has_enough_players(self):
        return len(self.players) >= Match.MIN_PLAYER

    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    @property
    def last_event(self):
        return self.log[-1]

    def publish(self, name, *args):
        seq = len(self.log)
        event = dict(seq=seq, name=name, args=args)
        self.log.append(event)


class GameOverException(Exception):
    pass


class Effect(ValueObject):

    def __init__(self, *args, **kwargs):
        self.owner_id = None
        self.card_index = None
        super(Effect, self).__init__(*args, **kwargs)

    def apply(self, match):
        owner = match.get_player_by_id(self.owner_id)
        card = owner.board[self.card_index]
        effects.apply(match, owner, card)
