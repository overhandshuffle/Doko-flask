from datetime import datetime

from doppelkopf import db
from doppelkopf.game_state import game_state
from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer, FinalScore


def append(json, gameId):
    for game in Game.query.all():

        if game.game_id == int(gameId):
            if (game.locked):
                # only un-locked games can be manipulated
                return False
            # welches format hat json???
            now = datetime.now()

            timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

            round = Rounds(game_id=gameId, timestamp=timestamp,
                           bock=json["bock"])
            db.session.add(round)
            db.session.commit()
            for user in json["spielerArray"]:

                if user["id"] == json["solo"]:
                    solo = "yes"
                else:
                    solo = "no"

                playerxround = RoundsXPlayer(
                    round_id=round.round_id,
                    user_id=user["id"],
                    punkte=user["punkte"],
                    partei=user["partei"],
                    solotyp=solo,
                    schweine=user["id"] == json["schweine"],
                    hochzeit=user["id"] == json["hochzeit"],
                    armut=user["id"] == json["armut"])

                db.session.add(playerxround)
                db.session.commit()
            return True

    return False


def lock(gameId):
    # set date for locked game
    for game in Game.query.all():
        if game.game_id == int(gameId):
            now = datetime.now()
            game.locked = now.strftime("%d/%m/%Y %H:%M:%S")
            db.session.commit()
            return True
    return False


def insert_finalscore(gameId):

    query = "Select game_id, player1_id, player2_id, player3_id, player4_id, player5_id FROM Game Where Game.game_id = " + \
        str(gameId)
    smt = db.engine.execute(query)
    for entry in smt:
        try:
            state = game_state(entry.game_id)["runden"][-1]["spielerArray"]
        except IndexError:
            return False

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
