from sqlalchemy import or_

from doppelkopf.database_constructors import Game, User, Rounds, RoundsXPlayer

player_ids=[2,7,8,9]

rounds=RoundsXPlayer.query.filter_by().all()
for r in rounds:
    print("lol")