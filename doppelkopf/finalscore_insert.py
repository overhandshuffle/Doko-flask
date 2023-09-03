from flask import jsonify

from sqlalchemy import or_
from doppelkopf import db

from doppelkopf.database_constructors import Game, User, Rounds, RoundsXPlayer, FinalScore
from doppelkopf.game_state import game_state
import time
from datetime import datetime


def insert_games():
    query = db.engine.execute(
        "Select game_id, player1_id, player2_id, player3_id, player4_id, player5_id FROM Game Where Game.locked IS NOT NULL;")
    for entry in query:
        try:
            state = game_state(entry.game_id)["runden"][-1]["spielerArray"]
        except IndexError:
            continue

        if entry.player5_id is not None:
            playerList2 = []
            scoreDict = {}
            for score in state:
                scoreDict[score["id"]] = score["zwischenstand"]
                playerList2.append(score["id"])
            for score in game_state(entry.game_id)["runden"][-2]["spielerArray"]:
                if score["id"] not in playerList2:
                    scoreDict[score["id"]] = score["zwischenstand"]

            game = FinalScore(game_id=entry.game_id,
                              player1_score=scoreDict[entry.player1_id],
                              player2_score=scoreDict[entry.player2_id],
                              player3_score=scoreDict[entry.player3_id],
                              player4_score=scoreDict[entry.player4_id],
                              player5_score=scoreDict[entry.player5_id])
            db.session.add(game)
            continue

        game = FinalScore(game_id=entry.game_id,
                          player1_score=state[0]["zwischenstand"],
                          player2_score=state[1]["zwischenstand"],
                          player3_score=state[2]["zwischenstand"],
                          player4_score=state[3]["zwischenstand"],
                          player5_score=None)

        db.session.add(game)
    db.session.commit()
