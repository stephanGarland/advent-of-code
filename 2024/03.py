import operator
import re
from typing import List

from utils import utilities
from utils.base_class import AbstractAOCD


class PartA(AbstractAOCD):
    """
    Find all instances of "mul(\\d+,\\d+)" in the test input.
    What are the sums of the products of each instance?
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = self.parse_input(self.aocd.puzzle)

    def parse_input(self, raw_data: List[str]):
        return "".join(raw_data)

    def get_muls(self) -> List[re.Match]:
        return list(re.finditer(r"(mul\((\d+,\d+)\))", self.data, re.MULTILINE))

    def solve(self):
        muls: List[str] = [x.groups()[-1] for x in self.get_muls()]
        return sum(
            operator.mul(*list(map(int, muls[i].split(",")))) for i in range(len(muls))
        )


class PartB(PartA):
    """
    Same problem as before, but anything following "don't()" is to be ignored,
    unless "do()" occurs to reset the logic.
    """

    def _get_mul_matches(self, s: str) -> List[str]:
        return re.findall(r"mul\((\d+),(\d+)\)", s)

    def _split_dos(self) -> List[str]:
        return self.data.split("do()")

    def _split_donts(self, s: str) -> str:
        return s.split("don't()")[0]

    def solve(self):
        products: List[int] = []
        dos_split: List[str] = self._split_dos()
        mul_matches: List[str] = []

        for ele in dos_split:
            mul_matches.extend(self._get_mul_matches(self._split_donts(ele)))

        for match in mul_matches:
            products.append(operator.mul(*(map(int, match))))

        return sum(products)


if __name__ == "__main__":
    args = utilities.parse_args()
    utilities.print_or_submit_solution(
        PartA, PartB, __file__, args.part, args.submit, args.debug
    )
