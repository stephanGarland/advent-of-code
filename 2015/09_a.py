from classes.template import AOCD as Base


class AOCD(Base):
    pass


class Solution:
    """

    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [int(x) if x else "" for x in self.aocd.puzzle]


if __name__ == "__main__":
    s = Solution()
