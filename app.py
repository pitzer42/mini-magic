from flask import Flask, jsonify, abort, request
import storage

app = Flask(__name__)


@app.route('/')
def index():
    storage.reset_database()
    return 'welcome to mini-magic'


@app.route('/api/v1.0/cards')
def list_cards():
    return jsonify(cards=storage.list_cards())


@app.route('/api/v1.0/cards/<int:card_id>', methods=['GET'])
def get_card(card_id):
    result = storage.get_card(card_id)
    if result is None:
        abort(404)
    return jsonify(result)


@app.route('/api/v1.0/decks')
def list_decks():
    return jsonify(decks=storage.list_decks())


@app.route('/api/v1.0/decks/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
    result = storage.get_deck(deck_id)
    if result is None:
        abort(404)
    return jsonify(result)


@app.route('/api/v1.0/matches', methods=['GET'])
def list_matches():
    return jsonify(matches=storage.list_matches())


@app.route('/api/v1.0/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    return jsonify(storage.get_match(match_id))


@app.route('/api/v1.0/matches', methods=['POST'])
def create_match():
    return jsonify(storage.create_match()), 201


@app.route('/api/v1.0/matches/<int:match_id>', methods=['POST'])
def join_match(match_id):
    if not request.json:
        abort(400)
    player_id = request.json['player_id']
    deck_id = request.json['deck_id']
    print(player_id, deck_id)
    return jsonify(storage.add_player_to_match(match_id, player_id, deck_id))


@app.route('/api/v1.0/matches/<int:match_id>/start', methods=['POST'])
def start_match(match_id):
    return jsonify(storage.start_match(match_id))


@app.route('/api/v1.0/matches/<int:match_id>/player/<int:player_id>/draw', methods=['GET'])
def draw(match_id, player_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
