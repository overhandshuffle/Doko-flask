import jwt
from doppelkopf import app, db
from doppelkopf import player, append_round, database_constructors


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)
