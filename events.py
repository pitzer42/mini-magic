Setup = 'setup'
PlayerJoin = 'player_join'
Ready = 'ready'
InitialDraw = 'initial_draw'
TurnBegin = 'turn_begin'
Refresh = 'refresh'
Draw = 'draw'
Prompt = 'prompt'
TurnEnd = 'turn_end'
GameOver = 'game_over'
Play = 'play'
Use = 'use'
Activate = 'activate'
Yield = 'yield'

SETUP_EVENT = dict(seq=0, name=Setup, args=list())


def publish(log, name, *args):
    seq = len(log)
    event = dict(seq=seq, name=name, args=args)
    log.append(event)