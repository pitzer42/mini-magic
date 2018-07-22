from flask import Flask, jsonify, abort, request, Response
import storage as storage
from entities import Match
import commands as commands
from commands import IllegalOperation
from functools import wraps

app = Flask(__name__)


def inject_json_fields(*fields):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if request.json is None:
                abort(400, description='json was expected in the request')
            for field in fields:
                if field not in request.json:
                    abort(400, description=field + ' field was expected in json request')
                kwargs[field] = request.json[field]
            return view(*args, **kwargs)
        return wrapped_view
    return decorator


def get_or_404(func, *args):
    doc = func(*args)
    if doc is None:
        abort(404)
    return doc


@app.route('/', methods=['GET'])
def index():
    storage.reset()
    return 'welcome to mini-magic'


@app.route('/cards', methods=['GET'])
def all_cards():
    items = get_or_404(storage.all_cards)
    return jsonify(items)


@app.route('/decks', methods=['GET'])
def all_decks():
    items = get_or_404(storage.all_decks)
    return jsonify(items)


@app.route('/players', methods=['GET'])
def all_players():
    items = get_or_404(storage.all_players)
    return jsonify(items)


@app.route('/matches', methods=['GET'])
def all_matches():
    items = get_or_404(storage.all_matches)
    return jsonify(items)


@app.route('/cards/<string:item_id>', methods=['GET'])
def get_card(item_id):
    item = get_or_404(storage.get_card, item_id)
    return jsonify(item)


@app.route('/decks/<string:item_id>', methods=['GET'])
def get_deck(item_id):
    item = get_or_404(storage.get_deck, item_id)
    return jsonify(item)


@app.route('/players/<string:item_id>', methods=['GET'])
def get_player(item_id):
    item = get_or_404(storage.get_player, item_id)
    return jsonify(item)


@app.route('/matches/<string:match_id>', methods=['GET'])
def get_match(match_id):
    match = get_or_404(storage.get_match, match_id)
    return jsonify(match)


@app.route('/matches/<string:match_id>/log', methods=['GET'])
def get_log(match_id):
    log = get_or_404(storage.get_log, match_id)
    return jsonify(log)


@app.route('/matches', methods=['POST'])
def create_match():
    match = Match()
    storage.add(match)
    return jsonify(match), 201


@app.route('/matches/<string:match_id>', methods=['POST'])
def create_match_with_id(match_id):
    match = Match(match_id)
    try:
        storage.add_match(match)
    except Exception:
        return Response(409)
    return jsonify(match), 201


@app.route('/matches/<string:match_id>/join', methods=['POST'])
@inject_json_fields('player_id', 'deck_id')
def join(match_id, player_id, deck_id):
    match = get_or_404(storage.get_match, match_id)
    player = get_or_404(storage.get_player, player_id)
    deck = get_or_404(storage.get_player, deck_id)
    try:
        match.join(player, deck)
    except IllegalOperation as e:
        message = str(e)
        print(message)
        abort(400, description=message)
    storage.update_match(match)
    return jsonify(match.to_dict())


@app.route('/matches/<string:match_id>/players/<int:player_index>/play/<int:card_index>', methods=['POST'])
def play(match_id, player_index, card_index):
    player_index -= 1
    card_index -= 1
    match = get_or_404(storage.get_match, match_id)
    try:
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


@app.route('/matches/<string:match_id>/players/<int:player_index>/use/<int:card_index>', methods=['POST'])
def use(match_id, player_index, card_index):
    player_index -= 1
    card_index -= 1
    match = get_or_404(storage.get_match, match_id)
    try:
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


@app.route('/matches/<string:match_id>/players/<int:player_index>/yield', methods=['POST'])
def yield_play(match_id, player_index):
    player_index -= 1
    match = get_or_404(storage.get_match, match_id)
    try:
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


if __name__ == '__main__':
    app.run(debug=True)
