from flask import Flask, jsonify, abort, request, Response
import storage
from models import Match, Player, Deck, Card, flatten

app = Flask(__name__)


@app.route('/')
def index():
    storage.reset()
    return 'welcome to mini-magic'


@app.route('/api/v1.0/cards')
def all_cards():
    return jsonify(cards=storage.all_cards())


@app.route('/api/v1.0/cards/<string:card_id>', methods=['GET'])
def get_card(card_id):
    result = storage.get_card(card_id)
    if result is None:
        abort(404)
    return jsonify(result)


@app.route('/api/v1.0/decks')
def list_decks():
    return jsonify(decks=storage.all_decks())


@app.route('/api/v1.0/decks/<string:deck_id>', methods=['GET'])
def get_deck(deck_id):
    result = storage.get_deck(deck_id)
    if result is None:
        abort(404)
    return jsonify(result)


@app.route('/api/v1.0/players', methods=['GET'])
def list_players():
    return jsonify(matches=storage.all_players())


@app.route('/api/v1.0/matches', methods=['GET'])
def list_matches():
    return jsonify(matches=storage.all_matches())


@app.route('/api/v1.0/matches/<string:match_id>', methods=['GET'])
def get_match(match_id):
    return jsonify(storage.get_match(match_id))


@app.route('/api/v1.0/matches', methods=['POST'])
def create_match():
    match = Match()
    match_dict = flatten(match)
    storage.insert_match(match_dict)
    return jsonify(match_dict), 201


@app.route('/api/v1.0/matches/<string:match_id>', methods=['POST'])
def join_match(match_id):
    if not request.json or 'player_id' not in request.json or 'deck_id' not in request.json:
        abort(400)
    try:
        player_id = request.json['player_id']
        deck_id = request.json['deck_id']

        player_dict = storage.get_player(player_id)
        deck_dict = storage.get_deck(deck_id)
        match_dict = storage.get_match(match_id)

        player = Player.create(player_dict)
        deck = Deck.create(deck_dict)
        match = Match.create(match_dict)

        last_card_id = None
        card_dict = None
        for card_id in deck.cards:
            if last_card_id is None or last_card_id != card_id:
                last_card_id = card_id
                card_dict = storage.get_card(card_id)
            card = Card.create(card_dict)
            player.deck.append(card)

        player.deck = deck.cards
        match.add_player(player)
        match_dict = flatten(match)

        storage.update_match(match_dict)
        return jsonify(match_dict)
    except Match.ImpossibleOperation:
        abort(400)


@app.route('/api/v1.0/matches/<string:match_id>/start', methods=['POST'])
def start_match(match_id):
    try:
        match_dict = storage.get_match(match_id)
        match = Match.create(match_dict)
        match.start()
        match_dict = flatten(match)
        match_dict = storage.update_match(match_dict)
        return jsonify(match_dict)
    except Match.ImpossibleOperation:
        abort(400)


@app.route('/api/v1.0/matches/<string:match_id>/player/<int:player_id>/draw', methods=['GET'])
def draw(match_id, player_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
