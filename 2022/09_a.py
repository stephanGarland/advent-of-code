from math import sqrt
from operator import sub

from classes.template import AOCD as Base
from classes.utilities import Utilities

SQRT_2 = sqrt(2)


class AOCD(Base):
    pass


class Solution:
    """
    Given a list of space-separated vectors representing the position
    of the head of a rope, find the number of unique positions that
    the tail of the rope will land on, if the tail must follow the head
    any time the distance between the head and tail exceeds 1. The tail
    can move orthogonally or diagonally.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [
            [int(y) if y.isdigit() else y for y in x.split()] for x in self.aocd.puzzle
        ]
        self.utilities = Utilities()

    # This heavily borrows from https://www.reddit.com/r/adventofcode/comments/zgnice/2022_day_9_solutions/j0cw2py/
    def solve(self, input_data: list[str, int]) -> int:
        move = {
            "R": complex(1, 0),
            "L": complex(-1, 0),
            "U": complex(0, 1),
            "D": complex(0, -1),
        }
        head = complex(0, 0)
        tail = complex(0, 0)
        visited = set()
        for direction, magnitude in input_data:
            for _ in range(magnitude):
                head += move[direction]
                diff = head - tail
                if abs(diff) > SQRT_2:
                    if diff.real != 0:
                        tail += diff.real / abs(diff.real)
                    if diff.imag != 0:
                        tail += complex(0, diff.imag) / abs(diff.imag)
                visited.add(tail)

        return len(visited)


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve(s.data))
