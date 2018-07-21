from flask import Flask, jsonify, abort, request, Response
import storage
import models
import game

app = Flask(__name__)


@app.route('/matches/<string:match_id>', methods=['GET'])
def get_match(match_id):
    match = storage.get_match(match_id)
    if match is None:
        abort(404)
    return jsonify(match)


@app.route('/matches/<string:match_id>/log', methods=['GET'])
def get_match_log(match_id):
    log = storage.get_log(match_id)
    if log is None:
        abort(404)
    return jsonify(log)


def require_fields_in_request_json(*args):
    if request.json is None:
        abort(400, description='json was expected in the request')
    for field in args:
        if field not in request.json:
            abort(400, description=field+' field was expected in json request')


@app.route('/matches/<string:match_id>/join', methods=['POST'])
def post_join_match(match_id):
    require_fields_in_request_json('player_id', 'deck_id')
    match = storage.get_match(match_id)
    if match is None:
        abort(404)
    player_id = request.json['player_id']
    deck_id = request.json['deck_id']
    player = storage.get_player(player_id)
    deck = storage.get_deck(deck_id)
    try:
        models.add_player_to_match(match, player, deck)
    except models.IllegalOperation as e:
        abort(400, description=str(e))
    storage.update_match(match)
    return jsonify(match)


@app.route('/matches/<string:match_id>/start', methods=['POST'])
def post_start_match(match_id):
    match = storage.get_match(match_id)
    try:
        models.start_match(match)
    except models.IllegalOperation:
        abort(400, description=str(e))
    game.update(match)
    storage.update_match(match)
    return jsonify(match)

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
