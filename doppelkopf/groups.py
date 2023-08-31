from flask import jsonify

from sqlalchemy import or_
from doppelkopf import db

from doppelkopf.database_constructors import Game, User, Rounds, RoundsXPlayer
from doppelkopf.game_state import game_state
import time
from datetime import datetime


def groups_all(user_id):
    anfang = time.time()

    auswertung2 = {}

    stmt = db.engine.execute("SELECT game.game_id, rounds.round_id, rounds_x_player.id, rounds_x_player.user_id, rounds_x_player.punkte, game.player1_id, game.player2_id, game.player3_id, game.player4_id, game.player5_id, game.timestamp FROM rounds JOIN rounds_x_player ON rounds.round_id = rounds_x_player.round_id JOIN game On game.game_id = rounds.game_id WHERE game.player1_id = 8 OR game.player2_id = 8 OR game.player3_id = 8 OR game.player4_id = 8 OR game.player5_id = 8 ORDER BY game.game_id DESC")
    ctr = 1
    lastgame = 0
    for entry in stmt:

        group_ids = []
        group_ids.append(entry.player1_id)
        group_ids.append(entry.player2_id)
        group_ids.append(entry.player3_id)
        group_ids.append(entry.player4_id)
        if entry.player5_id is not None:
            group_ids.append(entry.player5_id)

        group_ids = sorted(group_ids)
        if str(group_ids) not in auswertung2:

            rundenauswertung = {"spieler": {}}

            # leeres Json erstellen

            for id in group_ids:
                playerdata = {}
                playerdata["id"] = id
                playerdata["name"] = User.query.filter(
                    User.user_id == id).first().username
                playerdata["punkte"] = 0
                playerdata["position"] = 0
                rundenauswertung["spieler"][id] = playerdata

            rundenauswertung["rundenCount"] = 0
            auswertung2[str(group_ids)] = rundenauswertung
            auswertung2[str(group_ids)]["lastPlayed"] = datetime.strptime(
                entry.timestamp, '%d/%m/%Y %H:%M:%S').isoformat()
        if lastgame != entry.game_id:
            auswertung2[str(group_ids)]["rundenCount"] += 1

        auswertung2[str(group_ids)
                    ]["spieler"][entry.user_id]["punkte"] += entry.punkte

        lastgame = entry.game_id

    # print(auswertung2)

    for gr in auswertung2:

        endstaende = []

        for pl in auswertung2[gr]["spieler"]:

            endstaende.append(auswertung2[gr]["spieler"][pl]["punkte"])
        endstaende = sorted(endstaende, reverse=True)
        for pl in auswertung2[gr]["spieler"]:
            auswertung2[gr]["spieler"][pl]["position"] = endstaende.index(
                auswertung2[gr]["spieler"][pl]["punkte"])+1

    auswertungArray = []
    spielerArray = []
    for key in sorted(auswertung2, key=lambda k: (
            auswertung2[k]["rundenCount"], auswertung2[k]["lastPlayed"]), reverse=True):
        spielerArray = []
        for i in sorted(auswertung2[key]["spieler"], key=lambda k: (
                auswertung2[key]["spieler"][k]["position"])):
            spielerArray.append(auswertung2[key]["spieler"][i])

        auswertung2[key]["spieler"] = spielerArray
        auswertungArray.append(auswertung2[key])



    return (auswertungArray)
