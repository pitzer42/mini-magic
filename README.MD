# mini-magic

Simplified online multiplayer TCG with rule-enforcement. Playable through a Web API.

# To Do
  - front-end
  - authenicatated actions
  - AI
  - more cards
  - more game modes
  - define the rule subset
  - clients can get only unread logs from the match
  - clients can get only data they are allowed to see (ex: not each others hands)

# Game Structure
```
setup
^
|
v
player_join
|
v
ready
|
v
initial_draw
|
v
begin_turn
|
v
refresh
|
v
draw
|
v
prompt_current_player --> end_turn --> *begin_turn
|	|	|
v	v	v
play	use	yield
|_______|_______|
	|
	v
	prompt_other_player
________|________
|	|	|
play	use	yield
|_______|_______|
	|
	v
	*prompt_current_player
```

- setup: wait for player to join the match
- player_join: a new player joined the match
- ready: there are enough players to start the match
- initial_draw: players draw their initial hand
- begin_turn: one of the players becomes the current_player
- refresh: all cards in the board are back to their initial state
- draw: current_player draws a card
- prompt: wait for a player to take an action
- play: pay a cost to put a card from hand into board
- use: activate a card from the board
- yield: takes no action
- end_turn: the next_player becomes the current_player