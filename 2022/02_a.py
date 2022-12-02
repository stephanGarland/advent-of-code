from classes.template import AOCD as Base


class AOCD(Base):
    pass


class Solution:
    """
    Given a column with A (Rock), B (Paper), or C (Scissors),
    play the second column of X (Rock), Y (Paper), or Z (Scissors).

    Each round is scored for both for the outcome (win=6, draw=3, lose=0),
    and the shape you played (rock=1, paper=2, scissors=3).

    Return the total score of all rounds.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = ["".join(x.split()) for x in self.aocd.puzzle]

    def calculate(self):
        self.matchup_map = {
            "AX": 3,  # Rock == Rock         --> Draw
            "AY": 6,  # Rock < Paper         --> Win
            "AZ": 0,  # Rock > Scissors      --> Lose
            "BX": 0,  # Paper > Rock         --> Lose
            "BY": 3,  # Paper == Paper       --> Draw
            "BZ": 6,  # Paper < Scissors     --> Win
            "CX": 6,  # Scissors < Rock      --> Win
            "CY": 0,  # Scissors > Paper     --> Lose
            "CZ": 3,  # Scissors == Scissors --> Draw
        }

        self.shape_map = {
            "X": 1,  # Rock     = 1
            "Y": 2,  # Paper    = 2
            "Z": 3,  # Scissors = 3
        }

        return sum([*map(self.matchup_map.get, self.data)]), sum(
            [self.shape_map[x[1]] for x in self.data]
        )

    def solve(self):
        return sum(self.calculate())


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve())
