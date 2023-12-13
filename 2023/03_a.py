from itertools import takewhile

from more_itertools import peekable, seekable

from classes.template import AOCD as Base
from classes.utilities import Utilities


class AOCD(Base):
    pass


class Solution:
    """
    Given an input consisting of periods, numbers, and other symbols,
    find all numbers adjacent – orthogonally or diagonally – to
    a symbol, which is defined as anything not a number or period.
    Return the sum of all numbers meeting this criteria.
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

    def offsets_are_good(self, off: tuple[int, int], i: int, j: int) -> bool:
        try:
            if (
                self.data[i + off[0]][j + off[1]] != "."
                and not self.data[i + off[0]][j + off[1]].isdigit()
            ):
                return True
        except IndexError:
            pass
        return False

    def solve(self) -> int:
        numbers: list[int] = []
        for i, line in enumerate(self.data):
            for j, char in (it := peekable(enumerate(line))):
                if char.isdigit():
                    number_is_good = False
                    number = seekable(
                        takewhile(lambda x: x.isdigit(), self.data[i][j:])
                    )
                    number_len = sum(1 for _ in takewhile(str.isdigit, number))
                    number.seek(0)
                    for k in range(number_len):
                        if number_is_good:
                            break
                        for off in self.offsets:
                            if (j + k) == 0 and off[1] == -1:
                                continue
                            if number_is_good := self.offsets_are_good(off, i, (j + k)):
                                break
                    if number and number_is_good:
                        numbers.append(int("".join(number)))
                        try:
                            while True:
                                if not it.peek("EOF")[1].isdigit():
                                    break
                                else:
                                    next(it, None)
                        except TypeError:
                            break
        return sum(numbers)


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve())
