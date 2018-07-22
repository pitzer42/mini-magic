import log_list

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

publish = log_list.publish
