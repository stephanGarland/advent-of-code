import re
from functools import partial
from typing import List, Tuple

from utils import utilities
from utils.base_class import AbstractAOCD


class PartA(AbstractAOCD):
    """
    Find the number of instances that the string "XMAS" appears.
    It may be orthogonally contiguous, diagonally contiguous,
    or non-contiguous through other words; it may also be reversed.
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = self.parse_input(self.aocd.puzzle)

    def parse_input(self, raw_data: List[str]):
        return raw_data

    def get_orthogonal_count(self) -> int:
        regex = re.compile(r"(?=(XMAS|SAMX))")
        partial_findall = partial(re.findall, regex)
        num: int = 0
        for data in [self.data, utilities.transpose_list(self.data, join=True)]:
            num += sum([len(x) for x in (map(partial_findall, data)) if x])

        return num

    def get_diagonal_count(self) -> int:
        height: int = len(self.data)
        width: int = len(self.data[0])
        num: int = 0
        target_word: str = "XMAS"
        target_len = len(target_word)
        directions: List[Tuple[int, ...]] = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for row in range(height):
            for col in range(width):
                if self.data[row][col][0] != "X":
                    continue

                for move_row, move_col in directions:
                    if not (
                        0 <= row + (target_len - 1) * move_row < height
                        and 0 <= col + (target_len - 1) * move_col < width
                    ):
                        continue
                    for i in range(target_len):
                        cur_row = row + i * move_row
                        cur_col = col + i * move_col
                        if not self.data[cur_row][cur_col] == target_word[i]:
                            break
                    else:
                        num += 1
        return num

    def solve(self):
        return self.get_orthogonal_count() + self.get_diagonal_count()


class PartB(PartA):
    """
    Find the number of instances that the string "MAS" appears,
    in an "X". Each "MAS" instance can be forward or backward.
    """

    def get_diagonal_count(self) -> int:
        height: int = len(self.data)
        width: int = len(self.data[0])
        num: int = 0
        directions: List[Tuple[int, ...]] = [(-1, -1, 1, 1), (-1, 1, 1, -1)]

        for row in range(1, height - 1):
            for col in range(1, width - 1):
                if self.data[row][col] != "A":
                    continue

                for up_row, up_col, down_row, down_col in directions:
                    up_char = self.data[row + up_row][col + up_col]
                    down_char = self.data[row + down_row][col + down_col]

                    if not (
                        (up_char == "M" and down_char == "S")
                        or (up_char == "S" and down_char == "M")
                    ):
                        break
                else:
                    num += 1
        return num

    def solve(self):
        return self.get_diagonal_count()


if __name__ == "__main__":
    args = utilities.parse_args()
    utilities.print_or_submit_solution(
        PartA, PartB, __file__, args.part, args.submit, args.debug
    )
