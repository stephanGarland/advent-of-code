import itertools

from classes.template import AOCD as Base


class AOCD(Base):
    pass


class Solution:
    """
    Given blank-line separated groups of integers representing the amount
    of calories each elf is carrying, return the largest sum.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [int(x) if x else "" for x in self.aocd.puzzle]

    def group(self):
        elves = [
            list(g) for k, g in itertools.groupby(self.data, key=lambda x: x != "") if k
        ]
        return elves

    def solve(self):
        return max([sum(x) for x in self.group()])


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve())
