from copy import copy
from random import randint

from flask import Flask, jsonify, request

from ExecuteTest import Process
from GetChallenge import GetChallenge

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


class Teams(Process):
    def __init__(self, id: int, name: str, nb_users: int, challenge_id: int) -> None:
        super().__init__(challenge_id)
        self.id = id
        self.name = name
        self.nb_users = nb_users
        self.users = []

    def get_users(self) -> dict:
        return {"name": self.name, "id": self.id, "users": [i.get_user() for i in self.users]}

    def add_user(self, user: User) -> None:
        self.users.append(user)
        self.nb_users += 1

    def remove_user(self, id_user: int) -> None:
        for i in range(self.nb_users):
            if self.users[i].id == id_user:
                self.users[i].id_team = 0
                self.users.pop(i)
                self.nb_users -= 1
                break

    def get_nb_user(self) -> int:
        return len(self.users)


class Game:
    def __init__(self, nb_team: int, challenge_id: int = randint(0, 1)) -> None:
        t_name = copy(TEAMS_NAME)
        self.__challenge_id = challenge_id
        self.__get_challenge = GetChallenge(self.__challenge_id)
        self.nb_users = self.__get_challenge.get_public()["tests"]["nb_users"]
        self.teams = [Teams(i, next(t_name, None), 0, self.__challenge_id)
                      for i in range(nb_team + 1)]
        self.users = []
        self.nb_team = nb_team

    def add_user(self, id: int, name: int, id_team: int) -> bool:
        self.users.append(User(id, name, id_team))
        # self.teams[id_team].add

    def remove_user(self, user_id: int) -> None:
        for i in range(len(self.users)):
            if self.users[i].id == user_id:
                self.users.pop(i)
                [team.remove_user(user_id) for team in self.teams]

    def change_user_team(self, id_user: int, id_team: int):
        self.teams[self.users[id_user].id_team].remove_user(id_user)
        self.users[id_user].id_team = id_team
        self.users[id_user].part = self.teams[id_team].get_nb_player(
        ) % self.nb_users

    def get_team_with_user(self):
        # team = [i for i in self.teams if i.get_nb_user() != 0 and ]
        pass

    def get_team_user_id(self, id_user: int) -> User:
        for user in self.users:
            if user.id_user == id_user:
                return user.id_team


games = {}


@app.route('/user/<int:id_game>/<int:id_user>', methods=['POST', 'GET'])
def get_exec(id_game, id_user):
    data = request.json
    print(data, id_game, id_user)
    return jsonify(data)


@app.route('/game/<int:id_game>/<int:id_user>', methods=['GET'])
def create_game(id_game, id_user):
    if id_game in games:
        games[id_game].add_user(id_user, 0)
    else:
        games[id_game] = Game(2)
        games[id_game].add_user(id_user, 0)

    return jsonify()


@app.route('/game/<int:id_game>/<int:id_user>/<int:id_team>', methods=['GET'])
def change_team(id_game, id_user, id_team):
    if not games[id_game] or not games[id_game].teams[id_team] or not games[id_game].users[id_user]:
        return jsonify(None)
    games[id_game].change_user_team(id_user, id_team)
    return jsonify()


def delete_game(id_game: int) -> None:
    del games[id_game]


if __name__ == '__main__':
    app.run(debug=True)
