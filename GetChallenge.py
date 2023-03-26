from json import loads

class GetChallenge:
    def __init__(self, challenge: int) -> None:
        with open(f"challenge{challenge}.json", 'r') as fd:
            self.__challenge = loads(fd.read())
            fd.close()
        self.__private = self.__challenge.pop("final_tests")

    def get_tests(self, user: int) -> dict:
        return self.__challenge["tests"][f"user{user}"]

    def get_function_names(self) -> dict:
        nb_users = self.__challenge["tests"]["nb_users"]
        prototypes = {}
        for i in range(nb_users):
            prototypes[f"user{i}"] = self.__challenge["tests"][f"user{i}"]["prototype"]
        return prototypes

    def get_public(self) -> dict:
        return self.__challenge

    def get_private(self) -> dict:
        return self.__private