from app.validations import get_or_404

from flask import jsonify, abort
import storage as storage
from entities import Match


def index():
    storage.reset()
    return 'welcome to mini-magic'


def all_cards():
    items = get_or_404(storage.all_cards)
    return jsonify(items)


def all_decks():
    items = get_or_404(storage.all_decks)
    return jsonify(items)


def all_players():
    items = get_or_404(storage.all_players)
    return jsonify(items)


def all_matches():
    items = get_or_404(storage.all_matches)
    return jsonify(items)


def get_card(item_id):
    item = get_or_404(storage.get_card, item_id)
    return jsonify(item)


def get_deck(item_id):
    item = get_or_404(storage.get_deck, item_id)
    return jsonify(item)


def get_player(item_id):
    item = get_or_404(storage.get_player, item_id)
    return jsonify(item)


def get_match(item_id):
    match = get_or_404(storage.get_match, item_id)
    return jsonify(match)


def get_log(item_id):
    log = get_or_404(storage.get_log, item_id)
    return jsonify(log)


def create_match():
    match = storage.add_match(Match())
    return jsonify(match), 201


def create_match_with_id(match_id):
    match = Match(_id=match_id)
    try:
        storage.add_match(match)
    except:
        abort(409)
    return jsonify(match), 201