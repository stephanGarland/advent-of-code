import re

from classes.template import AOCD as Base


class AOCD(Base):
    pass


class Solution:
    """
    Given comma-separated pairs of ranges (e.g. 2-8,7-16), find the number of
    ranges where one range subsumes the other.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x if x else "" for x in self.aocd.puzzle]

    def subsumed_range(self, range_1, range_2, partial=False):
        """
        Returns: tuple(range: <is [partially] subsumed by> range)
        """

        def _operator():
            if partial:
                return any
            return all

        operator = _operator()
        if operator(e in range_1 for e in range_2):
            return (range_1, range_2)
        elif operator(e in range_2 for e in range_1):
            return (range_2, range_1)
        else:
            return None

    def make_range(self, range_list, inclusive=True):
        if inclusive:
            return range(range_list[0], range_list[1] + 1)

        return range(range_list[0], range_list[1])

    def range_subsumptions(self):
        subsumed_ranges = []
        for section in self.data:
            r_1, r_2 = [
                list(map(int, x.split("-"))) for x in re.findall("\d+-\d+", section)
            ]
            range_1 = self.make_range(r_1)
            range_2 = self.make_range(r_2)
            subsumed = self.subsumed_range(range_1, range_2, partial=True)
            if subsumed:
                subsumed_ranges.append((range_1, range_2))

        return subsumed_ranges

    def solve(self):
        return len(self.range_subsumptions())


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve())
