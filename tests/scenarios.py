from storage import _drop_all, add_card, add_deck, add_player, add_match
from entities import Resources, Card, Deck, Player, Match


def one_of_each_entity():
    _drop_all()
    add_card(Card(_id=1, name='Vanilla 1', cost=Resources(a=1), attack=1, defense=1))
    add_deck(Deck(_id=1, card_ids=['1', '2', '4', '3'] * 5))
    add_player(Player(_id=1))
    add_match(Match(_id=1))

