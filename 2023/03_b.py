from itertools import takewhile

from classes.template import AOCD
from classes.utilities import Utilities


class Solution:
    """
    Given an input consisting of periods, numbers, and other symbols,
    find all pairs of numbers that are adjacent – orthogonally or
    diagonally – to an asterisk. For every pair, calculate their product.
    Return the sum of all of these products.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x for x in self.aocd.puzzle]
        self.offsets = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        self.utilities = Utilities()

    def get_offsets(self, i: int, j: int) -> list[tuple[int]]:
        candidates = []
        for off in self.offsets:
            if (i + off[0] < 0) or (j + off[1] < 0):
                continue
            try:
                if self.data[i + off[0]][j + off[1]].isdigit():
                    candidates.append(off)
            except IndexError:
                pass

        # if all candidates are in the same row, and the x-position (j)
        # delta is less than the number of candidates, there cannot be
        # any symbols between digits, and a single long number has been found
        if len(set(list(x[0] for x in candidates))) == 1 and sum(
            map(abs, [x[1] for x in candidates])
        ) < len(candidates):
            return []
            # else return first and last sorted
        try:
            return sorted(candidates)[:: len(candidates) - 1]
        except ValueError:
            return []

    def get_offset_number(self, num_coords: list[int]) -> int:
        i, j = num_coords
        left = self.data[i][:j]
        right = self.data[i][j:]
        num_left = list(takewhile(lambda x: x.isdigit(), left[::-1]))[::-1]
        num_right = list(takewhile(lambda x: x.isdigit(), right))

        return int("".join(num_left + num_right))

    def get_multiplicand(self, i: int, j: int, offset_pair: tuple[int]) -> int:
        num_coords = [[i, j][x] + offset_pair[x] for x in range(2)]
        return self.get_offset_number(num_coords)

    def solve(self) -> int:
        numbers: list[int] = []
        for i, line in enumerate(self.data):
            for j, char in enumerate(line):
                if char == "*":
                    if found_offsets := self.get_offsets(i, j):
                        product = 1
                        for offset in found_offsets:
                            product *= self.get_multiplicand(i, j, offset)
                        numbers.append(product)
        return sum(numbers)


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve())
