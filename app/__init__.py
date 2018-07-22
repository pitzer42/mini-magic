from flask import Flask
import app.data_api as data_api
import app.game_api as game_api

app = Flask(__name__)

app.add_url_rule('/', view_func=data_api.index, methods=['GET'])
app.add_url_rule('/cards', view_func=data_api.all_cards, methods=['GET'])
app.add_url_rule('/decks', view_func=data_api.all_decks, methods=['GET'])
app.add_url_rule('/players', view_func=data_api.all_players, methods=['GET'])
app.add_url_rule('/matches', view_func=data_api.all_matches, methods=['GET'])

app.add_url_rule('/cards/<string:item_id>', view_func=data_api.get_card, methods=['GET'])
app.add_url_rule('/decks/<string:item_id>', view_func=data_api.get_deck, methods=['GET'])
app.add_url_rule('/players/<string:item_id>', view_func=data_api.get_player, methods=['GET'])
app.add_url_rule('/matches/<string:item_id>', view_func=data_api.get_match, methods=['GET'])
app.add_url_rule('/matches/<string:item_id>/log', view_func=data_api.get_log, methods=['GET'])

app.add_url_rule('/matches', view_func=data_api.create_match, methods=['POST'])
app.add_url_rule('/matches/<string:match_id>', view_func=data_api.create_match_with_id, methods=['PUT'])

app.add_url_rule('/matches/<string:match_id>/join', view_func=game_api.join, methods=['POST'])
app.add_url_rule('/matches/<string:match_id>/players/<int:player_index>/play/<int:card_index>', view_func=game_api.play, methods=['POST'])
app.add_url_rule('/matches/<string:match_id>/players/<int:player_index>/use/<int:card_index>', view_func=game_api.use, methods=['POST'])
app.add_url_rule('/matches/<string:match_id>/players/<int:player_index>/yield', view_func=game_api.yield_play, methods=['POST'])
app.add_url_rule('/matches/<string:match_id>/players/<int:player_index>/end_turn', view_func=game_api.end_turn, methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True)
