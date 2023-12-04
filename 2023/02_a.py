from classes.template import AOCD as Base
from classes.utilities import Utilities


class AOCD(Base):
    pass


class Solution:
    """
    Given inputs of RGB cubes pulled from a bag, which games would have been
    possible with only 12[R]13[G]14[B] cubes? Return the sum of the IDs of the
    possible games (the ID is a monotonic 1-indexed number).
    """

    LIMIT_RED = 12
    LIMIT_GRN = 13
    LIMIT_BLU = 14

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x for x in self.aocd.puzzle]
        self.utilities = Utilities()

    def game_parser(self, game_data: str) -> list:
        game_rounds = []
        game_data = game_data.split(":")[-1]
        game_data = game_data.split(";")
        game_data = [x.strip().split(", ") for x in game_data]
        for game in game_data:
            game_rounds.append({x.split(" ")[1]: int(x.split(" ")[0]) for x in game})
        return game_rounds

    def game_was_possible(self, rounds: list[dict[str, int]]) -> bool:
        for rnd in rounds:
            if (
                rnd.get("red", 0) > Solution.LIMIT_RED
                or rnd.get("green", 0) > Solution.LIMIT_GRN
                or rnd.get("blue", 0) > Solution.LIMIT_BLU
            ):
                return False
        return True


if __name__ == "__main__":
    s = Solution()
    games = []
    for i, game in enumerate(s.data, start=1):
        if s.game_was_possible(s.game_parser(game)):
            games.append(i)
    s.aocd.submit_puzzle(sum(games))
