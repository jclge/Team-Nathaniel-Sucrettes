from json import loads


class GetChallenge:
    def __init__(self, challenge: int):
        with open(f"challenge{challenge}.json", 'r') as fd:
            self.__challenge = loads(fd.read())
            fd.close()
        self.__private = self.__challenge.pop("final_tests")

    def get_public(self) -> dict:
        return self.__challenge

    def get_private(self) -> dict:
        return self.__private