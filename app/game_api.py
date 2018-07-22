from app.validations import get_or_404, inject_json_fields
from entities import Match, Player, Deck
import engine
import commands
from commands import IllegalOperation
from flask import jsonify, abort, Response
import storage as storage


@inject_json_fields('player_id', 'deck_id')
def join(match_id, player_id, deck_id):
    match = Match(get_or_404(storage.get_match, match_id))
    player = Player(get_or_404(storage.get_player, player_id))
    deck = Deck(get_or_404(storage.get_deck, deck_id))
    try:
        engine.connect(match)
        commands.add_player_to_match(match, player, deck)
    except IllegalOperation as e:
        message = str(e)
        print(message)
        abort(400, description=message)
    match_data = storage.update_match(match)
    return jsonify(match_data)


def play(match_id, player_index, card_index):
    player_index -= 1
    card_index -= 1
    match = Match(get_or_404(storage.get_match, match_id))
    try:
        engine.connect(match)
        commands.play_card(match, player_index, card_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    storage.update_match(match)
    return Response(status=200)


def use(match_id, player_index, card_index):
    player_index -= 1
    card_index -= 1
    match = get_or_404(storage.get_match, match_id)
    try:
        engine.connect(match)
        commands.use_card(match, player_index, card_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    storage.update_match(match)
    return Response(status=200)


def yield_play(match_id, player_index):
    player_index -= 1
    match = get_or_404(storage.get_match, match_id)
    try:
        engine.connect(match)
        commands.yield_play(match, player_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    storage.update_match(match)
    return Response(status=200)