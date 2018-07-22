import commands
from commands import IllegalOperation
from app.validations import inject_json_fields
from flask import abort, Response


@inject_json_fields('player_id', 'deck_id')
def join(match_id, player_id, deck_id):
    try:
        commands.join(match_id, player_id, deck_id)
    except IllegalOperation as e:
        message = str(e)
        print(message)
        abort(400, description=message)
    return Response(status=200)


def play(match_id, player_index, card_index):
    player_index -= 1
    card_index -= 1
    try:
        commands.play_card(match_id, player_index, card_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    return Response(status=200)


def use(match_id, player_index, card_index):
    player_index -= 1
    card_index -= 1
    try:
        commands.use_card(match_id, player_index, card_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    return Response(status=200)


def yield_play(match_id, player_index):
    player_index -= 1
    try:
        commands.yield_play(match_id, player_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    return Response(status=200)


def end_turn(match_id, player_index):
    player_index -= 1
    try:
        commands.end_turn(match_id, player_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    return Response(status=200)
