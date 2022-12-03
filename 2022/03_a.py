import collections
import string

from classes.template import AOCD as Base


class AOCD(Base):
    pass


class Solution:
    """
    Given lines of strings representing items in a sack, with each line being
    implicitly joined into two even sub-strings representing two compartments,
    find the common item in each sack between its two compartments.

    Then, map those to priorities of type {a-zA-Z: 1:52}, and sum them.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x if x else "" for x in self.aocd.puzzle]

    def count(self):
        self.priority_map = {}
        self.priority_map.update(zip(string.ascii_letters, range(1, 53)))
        rucksacks = collections.deque()
        for line in self.data:
            first_half = line[: len(line) // 2]
            second_half = line[len(line) // 2 :]
            most_common = "".join(set(first_half) & set(second_half))
            rucksacks.appendleft(most_common)

        return [self.priority_map[x] for x in rucksacks]

    def solve(self):
        return sum(self.count())


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve())
