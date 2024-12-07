from itertools import pairwise
from operator import sub
from typing import List, Tuple

from utils import utilities
from utils.base_class import AbstractAOCD


class PartA(AbstractAOCD):
    """
    Determine if each row is strictly monotonic. Additionally, any
    two adjacent values in a row must differ by 1 – 3, inclusive.
    What is the row count matching these requirements?
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = self.parse_input(self.aocd.puzzle)

    def parse_input(self, raw_data: List[str]):
        return [list(map(int, sub_list)) for sub_list in (x.split() for x in raw_data)]

    def check_levels(self, levels: List[List[int]]) -> int:
        MIN_DIFF: int = 1
        MAX_DIFF: int = 3
        is_inc: bool = False
        pairs: List[Tuple[int, ...]]
        safe_levels: int = 0
        for level in levels:
            # in testing there was no real difference in speed
            # but it seems wasteful to iterate through a failure
            if len(set(level)) != len(level):
                continue
            pairs = list(pairwise(level))
            is_inc = pairs[0][1] > pairs[0][0]
            for pair in pairs:
                # XOR – if strict monotonicity is broken, fail
                if (pair[1] > pair[0]) ^ is_inc:
                    break
                # 0 – 3 max diff
                if not MIN_DIFF <= abs(sub(*pair)) <= MAX_DIFF:
                    break
            else:
                safe_levels += 1
        return safe_levels

    def solve(self):
        return self.check_levels(self.data)


class PartB(PartA):
    """
    One digit from each row can be removed. If by doing so
    the row now meets the same critiera as before, it can be used.
    What is the row count matching these requirements?
    """

    def check_levels(self, levels: List[List[int]]) -> int:
        MAX_CHECKS: int = 1
        MIN_DIFF: int = 1
        MAX_DIFF: int = 3
        safe_levels: int = 0

        def _check_level(level: List[int], num_runs: int = 0) -> int:
            pairs: List[Tuple[int, ...]]
            if num_runs > MAX_CHECKS:
                return 0
            pairs = list(pairwise(level))
            if not pairs:
                return 1
            is_inc = pairs[0][1] > pairs[0][0]
            valid = True
            for pair in pairs:
                if (pair[1] > pair[0]) ^ is_inc:
                    valid = False
                    break
                elif not MIN_DIFF <= abs(sub(*pair)) <= MAX_DIFF:
                    valid = False
                    break
            if valid:
                return 1
            if num_runs == 0:
                for i in range(len(level)):
                    new_level = level[:i] + level[i + 1 :]
                    # because when has recursion ever gone wrong?
                    if _check_level(level=new_level, num_runs=1):
                        return 1
            return 0

        for level in levels:
            # can't do a len(set) check here, since we can remove one value
            safe_levels += _check_level(level)

        return safe_levels

    def solve(self):
        return self.check_levels(self.data)


if __name__ == "__main__":
    args = utilities.parse_args()
    utilities.print_or_submit_solution(
        PartA, PartB, __file__, args.part, args.submit, args.debug
    )
