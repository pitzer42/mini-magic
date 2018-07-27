def apply(match, owner, card):
    globals()[card.effect_id](match, owner, card)


def add_a(match, owner, card):
    owner.resources.a += 1


def add_b(match, owner, card):
    owner.resources.b += 1


def one_damage(match, owner, card):
    target = match.next_player(current=owner)
    target.hp -= 1


def counter(match, owner, card):
    match.stack.pop(-1)