from copy import copy

from flask import Flask, jsonify, request

app = Flask(__name__)


class User:
    def __init__(self, id, name, id_team):
        self.id = id
        self.name = name
        self.part = 0
        self.id_team = id_team

    def get_user(self):
        return {"id": self.id, "name": self.name, "part": self.part, "id_team": self.id_team}


TEAMS_NAME = ["no_team", "Blue", "Red", "Pink", "Orange", "Purple", "Green"]


class Teams:
    def __init__(self, id, name, nb_users) -> None:
        self.id = id
        self.name = name
        self.nb_users = nb_users
        self.users = []

    def get_users(self):
        return {"name": self.name, "id": self.id, "users": [i.get_user() for i in self.users]}


class Game:
    def __init__(self, subject, tests_verif, nb_team) -> None:
        t_name = copy(TEAMS_NAME)
        self.teams = [Teams(i, next(t_name, None)) for i in range(nb_team + 1)]
        self.users = []
        self.subject = subject
        self.tests_verif = tests_verif
        self.nb_team = nb_team

    def add_user(self, id, name, id_team) -> bool:
        self.users.append(User(id, name, id_team))

    


games = {}


@app.route('/user/<int:id_game>/<int:id_user>', methods=['POST', 'GET'])
def get_exec(id_game, id_user):
    data = request.json
    print(data, id_game, id_user)
    return jsonify(data)


@app.route('/game/<int:id_game>/<int:id_user>', methods=['GET'])
def create_game(id_game, id_user, id_team):
    if games[id_game]:
        games[id_game].add_user(id_user, id_team)
    else:
        games[id_game] = Game()

    return jsonify()


if __name__ == '__main__':
    app.run(debug=True)
