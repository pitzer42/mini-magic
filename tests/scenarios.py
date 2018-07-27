from storage import drop_all
from entities import Resources, Card, Deck, Player, Match


def one_of_each_entity():
    drop_all()
    Card(_id=1, name='Vanilla 1', cost=Resources(a=1), attack=1, defense=1).save()
    Deck(_id=1, card_ids=['1'] * 20).save()
    Player(_id=1).save()
    Match(_id=1).save()


def two_players():
    drop_all()
    Card(_id='1', name='Bolt', cost=Resources(a=1), effect_id='one_damage').save()
    Card(_id='2', name='Mana', cost=Resources(), effect_id='add_a').save()
    Card(_id='3', name='Counter', cost=Resources(), effect_id='counter').save()
    Deck(_id=1, card_ids=['1', '2'] * 10).save()
    Deck(_id=2, card_ids=['3'] * 20).save()
    Player(_id=1).save()
    Player(_id=2).save()

