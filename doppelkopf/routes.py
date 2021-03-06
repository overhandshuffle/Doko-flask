
from flask import render_template, url_for, flash, redirect, jsonify, request
from flask_api import status
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt, JWTManager, decode_token
from doppelkopf import create_game, jwt_login, database_constructors, player, app, append_round, game_state
import datetime


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # überprüfen ob Passwort korrekt ist
    if not jwt_login.password_check(username, password):
        return jsonify({"msg": "Bad username or password"}), 406

    # bei erfolgreicehr anmeldung Tokenübermittelung an Client
    access_token = create_access_token(
        identity=username, expires_delta=datetime.timedelta(hours=24))
    print(decode_token(access_token, allow_expired=False))
    return jsonify(access_token=access_token)

@app.route('/new', methods=["POST"])
@jwt_required()
def create_games():
    players = request.json
    create_game.create(players)
    return jsonify(create_game.create(players))


@app.route('/game/<gameId>', methods=["GET", "POST"])
@jwt_required()
def game(gameId):
    if request.method == 'POST':
        content = request.json
        if not append_round.append(content, gameId):
            return "gameID not found", status.HTTP_400_BAD_REQUEST

    return jsonify(game_state.game_state(gameId))


@app.route('/namelist/<name>', methods=["GET"])
@jwt_required()
def name_list(name):
    if len(name)>2:
        return ({"player": player.check_name(name)})
    else:
        return jsonify({"msg": "more characters"}), 406

@app.route('/new_player', methods=["POST"])
@jwt_required()
def new_player():
    username = request.json.get("username", None)
    added_from = get_jwt_identity()
    return player.add_new_player(added_from, username)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
