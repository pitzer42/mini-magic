from flask import Flask, jsonify, abort, request, Response
import storage
import models
from functools import wraps

app = Flask(__name__)


def require_json_fields(*fields):
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


def get_or_404(collection, _id):
    doc = storage.get_doc(collection, _id)
    if doc is None:
        abort(404)
    return doc


@app.route('/matches/<string:match_id>', methods=['GET'])
def get_match(match_id):
    match = storage.get_match(match_id)
    if match is None:
        abort(404)
    return jsonify(match)


@app.route('/matches/<string:match_id>/log', methods=['GET'])
def get_log(match_id):
    match = get_or_404('Matches', match_id)
    log = match['log']
    return jsonify(log=log)


@app.route('/matches/<string:match_id>', methods=['POST'])
def create_match_with_id(match_id):
    match = models.match(_id=match_id)
    try:
        storage.insert_match(match)
    except Exception:
        return Response(409)
    return jsonify(match)


@app.route('/matches', methods=['POST'])
def create_match():
    match = models.match()
    try:
        storage.insert_match(match)
    except Exception:
        return Response(400)
    return jsonify(match)


@app.route('/matches/<string:match_id>/join', methods=['POST'])
@require_json_fields('player_id', 'deck_id')
def join(match_id, player_id, deck_id):
    match = get_or_404('Matches', match_id)
    player = get_or_404('Players', player_id)
    deck = get_or_404('Decks', deck_id)
    models.MiniMagicEngine(match)
    try:
        models.add_player_to_match(match, player, deck)
    except models.IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    storage.update_match(match)
    return Response(status=200)


@app.route('/matches/<string:match_id>/players/<int:player_index>/play/<int:card_index>', methods=['POST'])
def play(match_id, player_index, card_index):
    player_index -= 1
    card_index -= 1
    match = get_or_404('Matches', match_id)
    models.MiniMagicEngine(match)
    try:
        models.play_card(match, player_index, card_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except models.IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    storage.update_match(match)
    return Response(status=200)


@app.route('/matches/<string:match_id>/players/<int:player_index>/use/<int:card_index>', methods=['POST'])
def use(match_id, player_index, card_index):
    player_index -= 1
    card_index -= 1
    match = get_or_404('Matches', match_id)
    models.MiniMagicEngine(match)
    try:
        models.use_card(match, player_index, card_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except models.IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    storage.update_match(match)
    return Response(status=200)


@app.route('/matches/<string:match_id>/players/<int:player_index>/yield', methods=['POST'])
def yield_play(match_id, player_index):
    player_index -= 1
    match = get_or_404('Matches', match_id)
    models.MiniMagicEngine(match)
    try:
        models.yield_play(match, player_index)
    except IndexError as error:
        error_message = str(error)
        print(error_message)
        abort(404, description=error_message)
    except models.IllegalOperation as error:
        error_message = str(error)
        print(error_message)
        abort(400, description=error_message)
    storage.update_match(match)
    return Response(status=200)




"""


# ________________________________________________________Data API

@app.route('/', methods=['GET'])
def index():
    storage.reset()
    return 'welcome to mini-magic'


@app.route('/api/v1.0/cards', methods=['GET'])
def get_all_cards():
    return jsonify(cards=storage.all_cards())


@app.route('/api/v1.0/decks', methods=['GET'])
def get_all_decks():
    return jsonify(decks=storage.all_decks())


@app.route('/api/v1.0/players', methods=['GET'])
def get_all_players():
    return jsonify(matches=storage.all_players())


@app.route('/api/v1.0/matches', methods=['GET'])
def get_all_matches():
    return jsonify(matches=storage.all_matches())


@app.route('/api/v1.0/cards/<string:card_id>', methods=['GET'])
def get_card(card_id):
    result = storage.get_card(card_id)
    if result is None:
        abort(404)
    return jsonify(result)


@app.route('/api/v1.0/decks/<string:deck_id>', methods=['GET'])
def get_deck(deck_id):
    result = storage.get_deck(deck_id)
    if result is None:
        abort(404)
    return jsonify(result)


@app.route('/api/v1.0/matches/<string:match_id>', methods=['GET'])
def get_match(match_id):
    result = storage.get_match(match_id)
    if result is None:
        abort(404)
    return jsonify(result)


# ________________________________________________________Game Logic

@app.route('/api/v1.0/matches', methods=['POST'])
def create_match():
    match = models.create_match()
    storage.insert_match(match)
    return jsonify(match), 201


@app.route('/api/v1.0/matches/<string:match_id>', methods=['POST'])
def join_match(match_id):
    if not request.json or 'player_id' not in request.json or 'deck_id' not in request.json:
        abort(400)
    try:
        player_id = request.json['player_id']
        deck_id = request.json['deck_id']
        player = storage.get_player(player_id)
        deck = storage.get_deck(deck_id)
        match = storage.get_match(match_id)
        models.add_player_to_match(match, player, deck)
        storage.update_match(match)
        return jsonify(match)
    except models.IllegalOperation:
        abort(400)


@app.route('/api/v1.0/matches/<string:match_id>/start', methods=['POST'])
def start_match(match_id):
    try:
        match = storage.get_match(match_id)
        models.start_match(match)
        storage.update_match(match)
        return jsonify(match)
    except models.IllegalOperation:
        abort(400)


@app.route('/api/v1.0/matches/<string:match_id>/draw', methods=['GET'])
def draw(match_id):
    try:
        match = storage.get_match(match_id)
        models.draw(match)
        storage.update_match(match)
        return jsonify(match)
    except models.IllegalOperation:
        abort(400)


@app.route('/api/v1.0/matches/<string:match_id>/players/<int:player_index>/hand/<int:card_index>/play', methods=['POST'])
def play(match_id, player_index, card_index):
    try:
        match = storage.get_match(match_id)
        models.play_card(match, player_index - 1, card_index - 1)
        storage.update_match(match)
        return jsonify(match)
    except models.IllegalOperation as error:
        abort(400, str(error))


@app.route('/api/v1.0/matches/<string:match_id>/players/<int:player_index>/board/<int:card_index>/use', methods=['POST'])
def use(match_id, player_index, card_index):
    try:
        match = storage.get_match(match_id)
        models.use_card(match, player_index - 1, card_index - 1)
        storage.update_match(match)
        return jsonify(match)
    except models.IllegalOperation as error:
        abort(400, str(error))


@app.route('/api/v1.0/matches/<string:match_id>/end_turn', methods=['POST'])
def end_turn(match_id):
    try:
        match = storage.get_match(match_id)
        models.end_turn(match)
        storage.update_match(match)
        return jsonify(match)
    except models.IllegalOperation as error:
        abort(400, str(error))
"""

if __name__ == '__main__':
    app.run(debug=True)
