from flask import Flask, jsonify, abort, request, Response
import storage
from models import Match, Player, Deck, Card, flatten, expand

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

        player = expand(Player, player_dict)
        deck = expand(Deck, deck_dict)
        match = expand(Match, match_dict)

        player.deck = list(deck.cards)
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
        match = expand(Match, match_dict)
        match.start()
        match_dict = flatten(match)
        match_dict = storage.update_match(match_dict)
        return jsonify(match_dict)
    except Match.ImpossibleOperation:
        abort(400)


@app.route('/api/v1.0/matches/<string:match_id>/players/<int:player_index>/draw', methods=['GET'])
def draw(match_id, player_index):
    match = expand(Match, storage.get_match(match_id))
    player = match.players[player_index - 1]
    card_id = player.deck.pop()
    card = expand(Card, storage.get_card(card_id))
    player.hand.append(card)
    storage.update_match(flatten(match))
    return jsonify(flatten(card))


if __name__ == '__main__':
    app.run(debug=True)
