from collections import Counter
from functools import partial
from operator import sub
from typing import Callable, List, Tuple

from utils import utilities
from utils.base_class import AbstractAOCD


class PartOne(AbstractAOCD):
    """
    Sort the left and right columns, and then calculate their difference pair-wise.
    What is the total sum of the pair differences?
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = self.parse_input(self.aocd.puzzle)

    def parse_input(self, raw_data: List[str]) -> List[List[int]]:
        return [list(map(int, sub_list)) for sub_list in (x.split() for x in raw_data)]

    def _apply_pairwise_transformation(
        self, operator: Callable, transformation: Callable, pair: Tuple[int, ...]
    ) -> int:
        return transformation(operator(*pair))

    def get_pair_diffs(self, cols: List[Tuple[int, ...]]) -> List[int]:
        get_abs_diff = partial(self._apply_pairwise_transformation, sub, abs)
        return list(map(get_abs_diff, cols))

    def solve(self) -> int:
        data_sorted = utilities.sort_columns_pairwise(self.data)
        return sum(self.get_pair_diffs(data_sorted))


class PartTwo(PartOne):
    """
    Sort the left and right columns, and then multiply each value in the left column
    by the number of times that value appears in the right column.
    What is the total sum of these products?
    """

    def solve(self) -> int:
        data_sorted = utilities.sort_columns_pairwise(self.data)
        cols = utilities.transpose_list(data_sorted)
        c = Counter(cols[1])
        s: int = 0
        for num in cols[0]:
            s += num * c.get(num, 0)

        return s


if __name__ == "__main__":
    args = utilities.parse_args()
    utilities.print_or_submit_solution(
        PartOne, PartTwo, __file__, args.part, args.submit
    )
