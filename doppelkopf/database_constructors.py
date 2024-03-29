import json

import bcrypt
from sqlalchemy import ForeignKey

from doppelkopf import db


class User(db.Model):
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100), nullable=False)
    password = db.Column("password", db.String(100), nullable=True)
    email = db.Column("email", db.String(100), nullable=True)
    added_from = db.Column("added_from", db.Integer,
                           ForeignKey("user.user_id"), nullable=True)
    last_login = db.Column("last_login", db.DATETIME, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Game(db.Model):
    game_id = db.Column("game_id", db.Integer, primary_key=True)
    timestamp = db.Column("timestamp", db.String(100), nullable=False)
    player1_id = db.Column(
        "player1_id", db.Integer, ForeignKey("user.user_id"), nullable=False
    )
    player2_id = db.Column(
        "player2_id", db.Integer, ForeignKey("user.user_id"), nullable=False
    )
    player3_id = db.Column(
        "player3_id", db.Integer, ForeignKey("user.user_id"), nullable=False
    )
    player4_id = db.Column(
        "player4_id", db.Integer, ForeignKey("user.user_id"), nullable=False
    )
    player5_id = db.Column(
        "player5_id", db.Integer, ForeignKey("user.user_id"), nullable=True
    )
    locked = db.Column(
        "locked", db.String(100), nullable=True
    )
    maxBock = db.Column(
        "maxBock", db.Integer
    )
    soloKommtRaus = db.Column(
        "soloKommtRaus", db.BOOLEAN
    )


class Rounds(db.Model):
    game_id = db.Column("game_id", db.Integer, ForeignKey("game.game_id"))
    round_id = db.Column("round_id", db.Integer, primary_key=True)
    timestamp = db.Column("timestamp", db.String(100), nullable=False)
    bock = db.Column("bock", db.BOOLEAN, nullable=False, default=False)


class RoundsXPlayer(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    round_id = db.Column("round_id", db.Integer, ForeignKey("rounds.round_id"))
    user_id = db.Column("user_id", db.Integer, ForeignKey("user.user_id"))
    punkte = db.Column("punkte", db.Integer)
    partei = db.Column("partei", db.String(100))
    hochzeit = db.Column("hochzeit", db.String(100), nullable=True)
    schweine = db.Column("schweine", db.String(100), nullable=True)
    armut = db.Column("armut", db.Integer, nullable=True)
    solotyp = db.Column("solotyp", db.String(100), nullable=True)


class FinalScore(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    game_id = db.Column("game_id", db.Integer, ForeignKey("game.game_id"))
    player1_score = db.Column("player1_score", db.Integer, nullable=False)
    player2_score = db.Column("player2_score", db.Integer, nullable=False)
    player3_score = db.Column("player3_score", db.Integer, nullable=False)
    player4_score = db.Column("player4_score", db.Integer, nullable=False)
    player5_score = db.Column("player5_score", db.Integer, nullable=True)


# only creates db if not existing
db.create_all()

# create admin user if user table is empty
if len(User.query.all()) == 0:
    hashed = bcrypt.hashpw("1234".encode(
        'UTF-8'), bcrypt.gensalt()).decode("utf-8")
    test = User(username="admin", added_from=None, password=hashed)
    db.session.add(test)
    db.session.commit()
