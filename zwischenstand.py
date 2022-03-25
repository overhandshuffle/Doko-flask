from doppelkopf.database_constructors import Game, Rounds, RoundsXPlayer, User
from doppelkopf import db
import json
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
import numpy as np


def chart(game_id):
    game = Game.query.filter_by(game_id=game_id).first()

    players = [game.player1_id, game.player2_id,
               game.player3_id, game.player4_id]

    if game.player5_id != None:
        players.append(game.player5_id)
    names = []
    for i, player in enumerate(players):
        pl = User.query.filter_by(user_id=player).first()
        names.append(pl.username)
    print(names)
    points = []
    for i in range(len(names)):
        points.append([0])
    x = [0]
    for n, round in enumerate(Rounds.query.filter_by(game_id=game_id).all()):
        for i, data in enumerate(RoundsXPlayer.query.filter_by(round_id=round.round_id).all()):
            points[i].append(data.punkte)
        x.append(n+1)
    l=len(x)
    for n, user_points in enumerate(points):
        for i in range(1, len(user_points)):
            user_points[i] = user_points[i]+user_points[i-1]

        
        xi = np.linspace(0, l, l*10)
        ius = InterpolatedUnivariateSpline(x, user_points)
        yi = ius(xi)
        #plt.plot(x, user_points, 'bo')
        plt.plot(xi, yi, label=names[n])

    print(points)
    plt.xlabel('Runden')
    plt.ylabel('Punkte')

    plt.title("Doko Punkteübersicht vom Spiel am "+ game.timestamp)
    plt.axhline(y=0, color='k')
  

    plt.legend()

    plt.show()
