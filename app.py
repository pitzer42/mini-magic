from flask import Flask, jsonify, abort

app = Flask(__name__)

decks = [
    [1, 1, 1],
    [1, 2, 2],
]

cards = [
    {
        'id': 0,
        'name': 'Vanilla 0',
        'cost':
            {
                'a':1,
                'b':0,
                'c':0
             },
        'attack': 1,
        'defense': 1,
        'tapped': False
    },
    {
        'id': 1,
        'name': 'Vanilla 2',
        'cost':
            {
                'a':1,
                'b':1,
                'c':0
             },
        'attack': 2,
        'defense': 2,
        'tapped': False
    }
]


@app.route('/')
def index():
    return 'welcome to mini-magic'


@app.route('/api/v1.0/cards')
def get_cards():
    return jsonify(cards=cards)


@app.route('/api/v1.0/cards/<int:card_id>', methods=['GET'])
def get_card(card_id):
    result = [card for card in cards if card['id'] == card_id]
    if len(result) == 0:
        abort(404)
    return jsonify(card=result[0])


@app.route('/api/v1.0/decks')
def get_decks():
    return jsonify(decks=decks)


@app.route('/api/v1.0/decks/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
    if deck_id < 0 or deck_id > len(decks):
        abort(404)
    else:
        return jsonify(deck=decks[deck_id])


if __name__ == '__main__':
    app.run(debug=True)