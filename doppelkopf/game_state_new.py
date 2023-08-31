from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer, User
import time

def game_state_new(game_id):
    anfang = time.time()
    game = Game.query.filter_by(game_id=game_id).first()
    
    gamestate = {
        "_id": game_id,
        "runden": [],
        "spieler": [],
        "remainingBock": [],
        "gesperrt": game.locked,
        "withoutBock": game.maxBock == 0,
        "timestamp": game.timestamp}
    
    players = [game.player1_id, game.player2_id,
               game.player3_id, game.player4_id]
    maxbock = game.maxBock
    aus = 6
    zs = [0, 0, 0, 0]
    
    remBock = [0] * 4
    solo_count = 0

    if game.player5_id is not None:
        players.append(game.player5_id)
        zs.append(0)
        
        aus = Rounds.query.filter_by(game_id=game_id).count() % len(players)
        remBock = [0] * 5
    
    for n, round in enumerate(Rounds.query.filter_by(game_id=game_id).all()):
        bock = remBock[0]
        remBock.pop(0)
        remBock.append(0)

        bock_counter = len(players)
        if round.bock == 1:
            for ind, el in enumerate(remBock):
                if bock_counter == 0:
                    break
                if el < maxbock:
                    bock_counter -= 1
                    remBock[ind] += 1
            for i in range(bock_counter):
                remBock.append(1)

    
        aussetzen = 6
        if len(players) == 5:
            aussetzen = n % len(players)

        roundstate = {
            "punkte": 0,
            "solo": None,
            "spielerArray": [],
            "bock": bock
        }







    print(time.time()-anfang)
   

        