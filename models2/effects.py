def apply(match, owner, card, effect_id):
    {
        'add_a': add_a,
        'add_b': add_b,
        '1_damage': one_damage
    }[effect_id](match, owner, card)


def add_a(match, owner, card):
    owner['resources']['a'] += 1


def add_b(match, owner, card):
    owner['resources']['b'] += 1


def one_damage(match, owner, card):
    for player in match['players']:
        if player['_id'] != owner['_id']:
            player['health_points'] -= 1
            return
