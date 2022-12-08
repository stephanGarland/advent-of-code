import more_itertools

from classes.template import AOCD as Base
from classes.utilities import Utilities

class AOCD(Base):
    pass


class Solution:
    """

    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x if x else "" for x in self.aocd.puzzle]
        self.data_list = list("".join(self.data))
        self.utilities = Utilities()

    def solve(self):
        window_size = 4
        datastream = more_itertools.sliding_window(self.data_list, window_size)

        return self.utilities.find_first_unique_window(datastream, window_size, inclusive=True)


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve())

