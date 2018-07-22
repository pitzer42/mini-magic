from flask import jsonify, abort
from app.validations import get_or_404
import storage as storage
from entities import Card, Player, Deck, Match


def index():
    storage.drop_all()
    return 'welcome to mini-magic'


def all_cards():
    items = get_or_404(storage.all_docs, Card.STORAGE_NAME)
    return jsonify(items)


def all_decks():
    items = get_or_404(storage.all_docs, Deck.STORAGE_NAME)
    return jsonify(items)


def all_players():
    items = get_or_404(storage.all_docs, Player.STORAGE_NAME)
    return jsonify(items)


def all_matches():
    items = get_or_404(storage.all_docs, Match.STORAGE_NAME)
    return jsonify(items)


def get_card(item_id):
    item = get_or_404(storage.get_doc, Card.STORAGE_NAME, item_id)
    return jsonify(item)


def get_deck(item_id):
    item = get_or_404(storage.get_doc, Deck.STORAGE_NAME, item_id)
    return jsonify(item)


def get_player(item_id):
    item = get_or_404(storage.get_doc, Player.STORAGE_NAME, item_id)
    return jsonify(item)


def get_match(item_id):
    item = get_or_404(storage.get_doc, Match.STORAGE_NAME, item_id)
    return jsonify(item)


def get_log(item_id):
    item = get_or_404(storage.get_doc, Match.STORAGE_NAME, item_id)
    return jsonify(log=item['log'])


def create_match():
    match = Match()
    match.save()
    return jsonify(match.to_dict()), 201


def create_match_with_id(match_id):
    match = Match()
    try:
        match.save()
    except:
        abort(409)
    return jsonify(match.to_dict()), 201