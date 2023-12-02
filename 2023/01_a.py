from classes.template import AOCD as Base
from classes.utilities import Utilities


class AOCD(Base):
    pass


class Solution:
    """
    Combine the first and last number in each line to form a 2-digit number.
    What is the sum of these numbers?
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x for x in self.aocd.puzzle]
        self.utilities = Utilities()

    def get_first_last(self, line: str) -> int:
        digits = [x for x in line if x.isdigit()]
        return int(f"{digits[0]}{digits[-1]}")

    def solve(self):
        return sum([self.get_first_last(x) for x in self.data])


if __name__ == "__main__":
    s = Solution()
    print(s.solve())
