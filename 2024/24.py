from typing import List

from utils import utilities
from utils.base_class import AbstractAOCD


class PartA(AbstractAOCD):
    """
    Placeholder docstring for Day 24 Part A.
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = self.parse_input(self.aocd.puzzle)

    def parse_input(self, raw_data: List[str]):
        pass

    def solve(self):
        pass


class PartB(PartA):
    """
    Placeholder docstring for Day 24 Part B.
    """

    def solve(self):
        pass


if __name__ == "__main__":
    args = utilities.parse_args()
    utilities.print_or_submit_solution(
        PartA, PartB, __file__, args.part, args.submit, args.debug
    )
