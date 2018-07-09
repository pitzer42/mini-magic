from flask import Flask, jsonify, abort, request
import storage

app = Flask(__name__)


@app.route('/')
def index():
    storage.setup()
    return 'welcome to mini-magic'


@app.route('/api/v1.0/cards')
def list_cards():
    return jsonify(cards=storage.list_cards())


@app.route('/api/v1.0/cards/<int:card_id>', methods=['GET'])
def get_card(card_id):
    result = storage.get_card(card_id)
    if result is None:
        abort(404)
    return jsonify(card=result)


@app.route('/api/v1.0/decks')
def list_decks():
    return jsonify(decks=storage.list_decks())


@app.route('/api/v1.0/decks/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
    result = storage.get_deck(deck_id)
    if result is None:
        abort(404)
    return jsonify(deck=result)


@app.route('/api/v1.0/matches', methods=['POST'])
def create_match():
    if not request.json:
        abort(400)
    new_match = dict()
    new_match['deck'] = request.json['deck']
    new_match['id'] = storage.create_match(new_match)
    return jsonify(match=new_match), 201


@app.route('/api/v1.0/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    return jsonify(match=storage.get_match(match_id))

@app.route('/api/v1.0/matches/<int:match_id>/player/<int:player_id>/draw', methods=['GET'])
def draw(match_id, player_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
