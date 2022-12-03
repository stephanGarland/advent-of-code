import collections
import itertools
import string


from classes.template import AOCD as Base


class AOCD(Base):
    pass


class Solution:
    """
    Given lines of strings representing items in a sack, find the common
    item in each sequential group of three sacks.

    Then, map those to priorities of type {a-zA-Z: 1:52}, and sum them.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x if x else "" for x in self.aocd.puzzle]

    # https://stackoverflow.com/a/22045226/4221094
    def make_group(self, iterator, group_size):
        it = iter(iterator)
        return list(iter(lambda: tuple(itertools.islice(it, group_size)), ()))

    def count(self):
        self.priority_map = {}
        self.priority_map.update(zip(string.ascii_letters, range(1, 53)))
        elf_groups = collections.deque()
        for groups in self.make_group(self.data, 3):
            most_common = "".join(set.intersection(*map(set, groups)))
            elf_groups.appendleft(most_common)

        return [self.priority_map[x] for x in elf_groups]

    def solve(self):
        return sum(self.count())


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve())
