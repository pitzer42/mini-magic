from models import Events
import models

INITIAL_HAND_SIZE = 7


def update(match):
    try:
        {
            Events.Ready: handle_ready,
        }[models.last_event(match)](match)
    except models.GameOverException:
        handle_game_over(match)


def handle_ready(match):
    draw_initial_hands(match)
    begin_turn(match)


def draw_initial_hands(match):
    models.log_event(match, models.Events.InitialDraw)
    for player in match['players']:
        models.draw(player, INITIAL_HAND_SIZE)


def begin_turn(match):
    models.log_event(match, models.Events.Refresh)
    player = models.current_player(match)
    for card in player['board']:
        card['activated'] = False
    models.log_event(match, models.Events.Draw, player['_id'])
    models.log_event(match, models.Events.Prompt, player['_id'])


def handle_game_over(match):
    models.log_event(match, models.Events.GameOver)


