from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer, User
import json


def game_state(game_id):
    game = Game.query.filter_by(game_id=game_id).first()
    gamestate = {
        "_id": game_id,
        "runden": [],
        "spieler": [],
        "timestamp": game.timestamp}

    # this section is for player related information
    players = [game.player1_id, game.player2_id,
               game.player3_id, game.player4_id]

    aus = 6
    zs = [0, 0, 0, 0]
    bock = [0, 0, 0, 0]
    if game.player5_id != None:
        players.append(game.player5_id)
        aus = len(Rounds.query.filter_by(game_id=game_id).all()) % len(players)
        zs.append(0)
        bock.append(0)

    raus = (len(Rounds.query.filter_by(game_id=game_id).all())+1) % len(players)

    for i, player in enumerate(players):
        pl = User.query.filter_by(user_id=player).first()
        name = pl.username

        if i == raus:
            outi = True
        else:
            outi = False
        if i == aus and aus != 6:
            auss = True
        else:
            auss = False
        spielerer = {
            "aussetzen": auss,
            "id": player,
            "kommt_raus": outi,
            "name": name
        }

        gamestate["spieler"].append(spielerer)

    for n, round in enumerate(Rounds.query.filter_by(game_id=game_id).all()):
        bock.pop(0)
        bock.append(round.bock)
        bock_sum = sum(bock)
        aussetzen = 6
        if len(players) == 5:
            aussetzen = n % len(players)

        roundstate = {
            "punkte": 0,
            "solo": None,
            "spielerArray": [],
            "bock": bock_sum
        }

        for i, data in enumerate(RoundsXPlayer.query.filter_by(round_id=round.round_id).all()):
            
            
            if i>=aussetzen:
                i+=1
           
            zs[i] += data.punkte
            player_state = {
                "id": data.user_id,
                "partei": data.partei,
                "punkte": data.punkte,
                "zwischenstand": zs[i]
            }
            if data.solotyp == "yes":
                roundstate["solo"] = data.user_id
            roundstate["punkte"] = abs(data.punkte)
            roundstate["spielerArray"].append(player_state)
        gamestate["runden"].append(roundstate)
    
    return gamestate
