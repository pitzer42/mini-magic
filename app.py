from flask import Flask, jsonify, abort, request
import models2.storage as storage
import models
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


def get_or_404(func, _id):
    doc = func(_id)
    if doc is None:
        abort(404)
    return doc


@app.route('/matches/<string:match_id>', methods=['GET'])
def get_match(match_id):
    match = get_or_404(storage.get_match, match_id)
    return jsonify(match.to_dict())


@app.route('/matches/<string:match_id>/log', methods=['GET'])
def get_log(match_id):
    log = get_or_404(storage.get_log, match_id)
    return jsonify(log.to_dict())


@app.route('/api/v1.0/matches', methods=['POST'])
def create_match():
    match = models.create_match()
    storage.insert_match(match)
    return jsonify(match), 201


@app.route('/matches/<string:match_id>/join', methods=['POST'])
@inject_json_fields('player_id', 'deck_id')
def join(match_id, player_id, deck_id):
    match = get_or_404(storage.get_match, match_id)
    player = get_or_404(storage.get_player, player_id)
    deck = get_or_404(storage.get_player, deck_id)
    try:
        match.join(player, deck)
    except models.IllegalOperation as e:
        message = str(e)
        print(message)
        abort(400, description=message)
    storage.update_match(match)
    return jsonify(match.to_dict())


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


if __name__ == '__main__':
    app.run(debug=True)
