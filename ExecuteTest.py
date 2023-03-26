from random import randint
from io import StringIO
from contextlib import redirect_stdout

from GetChallenge import GetChallenge


class Game:
    def __init__(self) -> None:
        self.__challenge = GetChallenge(randint(0, 0))
        self.__stdout = StringIO()
        self.__functions: dict = self.__challenge.get_function_names()

    def get_output(self, user: int, code: str) -> dict:
        res = {}
        tests = self.__challenge.get_tests(user)

        for i in range(tests["nb_tests"]):
            with redirect_stdout(self.__stdout):
                exec(code, locals())
                tryout = locals()[self.__functions[f'user{user}'][4:self.__functions[f'user{user}'].index('(')]]
                res["return"] = tryout(*tuple(tests[f"test{i}"]["input"]))
            res["code"] = self.__stdout.getvalue()
            return res


g = Game()
with open("test.txt", 'r') as fd:
    fun = fd.read()
    print(g.get_output(0, fun))
