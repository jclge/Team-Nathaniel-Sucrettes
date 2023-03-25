from json import loads


class GetChallenge:
    def __init__(self, challenge: int):
        with open(f"challenge{challenge}.json", 'r') as fd:
            self.__challenge = loads(fd.read())

    def get_public(self) -> dict:
        self.__challenge
        return

g = GetChallenge(0)