from random import randint
from io import StringIO
from contextlib import redirect_stdout
from copy import copy

from GetChallenge import GetChallenge


class Game:
    def __init__(self, challenge:int = randint(0, 1)) -> None:
        self.__challenge_id = challenge
        self.__challenge = GetChallenge(self.__challenge_id)
        self.__functions: dict = self.__challenge.get_function_names()

    def get_output(self, user: int, code: str) -> dict:
        res = {"return": [], "code": []}
        tests = self.__challenge.get_tests(user)

        for i in range(tests["nb_tests"]):
            stdout = StringIO()
            with redirect_stdout(stdout):
                try:
                    exec(code, locals())
                    tryout = locals()[self.__functions[f'user{user}'][4:self.__functions[f'user{user}'].index('(')]]
                    if type(tests[f"test{i}"]["input"]) is list:
                        res["return"].append(tryout(*tuple(tests[f"test{i}"]["input"])))
                    else:
                        res["return"].append(tryout(tests[f"test{i}"]["input"]))
                except Exception as e:
                    res["return"].append(1)
                    res["code"].append(e)
                    stdout.close()
                    return res
                res["code"].append(stdout.getvalue())
            stdout.close()
            if res["return"][-1] != tests[f"test{i}"]["output"]:
                return res
        return res

    def __prepare_final_call(self, codes, name) -> tuple:
        call_ = "tmp = " + name
        funcs = []

        for i in range(self.__challenge.get_public()["tests"]["nb_users"]):
            try:
                exec(codes[i], locals())
            except Exception as e:
                return None, None
            funcs.append(locals()[self.__functions[f'user{i}'][4:self.__functions[f'user{i}'].index('(')]])
            call_ = call_.replace(self.__functions[f'user{i}'][4:self.__functions[f'user{i}'].index('(')], f"funcs[{i}]")

        return call_, funcs

    def final_tests(self, codes: list[str]) -> dict:
        final_tests = self.__challenge.get_private()
        res = {"result": []}
        call_, funcs = self.__prepare_final_call(codes, final_tests["how_is_it_called"])
        if call_ is None:
            for _ in range(final_tests["nb_tests"]):
                res["result"].append(False)
            return res

        for j in range(final_tests["nb_tests"]):
            call_tmp = copy(call_)
            for i in range(final_tests["nb_variables"]):
                call_tmp = call_tmp.replace(f"arg{i}", str(final_tests[f"test{j}"]["variables"][f"arg{i}"]))
            loc = {}
            try:
                exec(call_tmp, locals(), loc)
                if loc["tmp"] == final_tests[f"test{j}"]["output"]:
                    res["result"].append(True)
                else:
                    res["result"].append(False)
            except Exception as e:
                res["result"].append(False)
        return res

    def get_public(self) -> dict:
        return self.__challenge.get_public()

    def get_challenge_id(self) -> int:
        return self.__challenge_id
