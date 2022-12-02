from importlib import import_module

PartOne = import_module("01_a", "Solution")


class Solution:
    """
    Given blank-line separated groups of integers representing the amount
    of calories each elf is carrying, return the sum of the largest three groups.
    """

    def __init__(self):
        self.part_one = PartOne.Solution()

    def solve(self):
        return sum(sorted([sum(x) for x in self.part_one.group()], reverse=True)[:3])


if __name__ == "__main__":
    s = Solution()
    s.part_one.aocd.submit_puzzle(s.solve())
