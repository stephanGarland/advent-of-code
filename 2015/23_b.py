from classes.template import AOCD as Base
from classes.utilities import Utilities

class AOCD(Base):
    pass


class Solution:
    """

    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x for x in self.aocd.puzzle]
        self.utilities = Utilities()


if __name__ == "__main__":
    s = Solution()

