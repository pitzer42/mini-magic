from storage import _drop_all, add_card, add_deck, add_player, add_match
from entities import Resources, Card, Deck, Player, Match


def one_of_each_entity():
    _drop_all()
    add_card(Card(_id=1, name='Vanilla 1', cost=Resources(a=1), attack=1, defense=1))
    add_deck(Deck(_id=1, card_ids=['1'] * 20))
    add_player(Player(_id=1))
    add_match(Match(_id=1))


def two_players():
    _drop_all()
    add_card(Card(_id='1', name='Bolt', cost=Resources(a=1), effect_id='1_damage'))
    add_card(Card(_id='2', name='Mana', cost=Resources(), effect_id='add_a'))
    add_deck(Deck(_id=1, card_ids=['1', '2'] * 10))
    add_player(Player(_id=1))
    add_player(Player(_id=2))

