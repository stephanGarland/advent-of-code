import re
from enum import Enum
from itertools import chain

from classes.template import AOCD as Base
from classes.utilities import Utilities

NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


class AOCD(Base):
    pass


class Position(Enum):
    FIRST = 0
    LAST = -1


class Solution:
    """
    Combine the first and last number in each line to form a 2-digit number.
    Note that a number may be a digit, or letters to spell a digit, e.g. 'nine'.
    What is the sum of these numbers?
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x for x in self.aocd.puzzle]
        self.utilities = Utilities()

    def find_all_indices(self, string, substring):
        pattern = re.escape(substring)
        indices = [match.span() for match in re.finditer(pattern, string)]
        return [indices] if indices else [[-1]]

    def get_nth_index(self, index_map: list[tuple], position: Enum) -> list[tuple]:
        return [x[position.value] for x in index_map]

    def find_first_and_last_number(self, line: str) -> tuple[int, int]:
        number_map = list(
            chain(*[self.find_all_indices(line, x) for x in NUMBERS.keys()])
        )
        digit_map = list(
            chain(*[self.find_all_indices(line, str(x)) for x in NUMBERS.values()])
        )
        result_map = list(zip(number_map, digit_map))

        number_indices = self.get_nth_index(result_map, Position.FIRST)
        digit_indices = self.get_nth_index(result_map, Position.LAST)

        number_indices = [
            x for x in list(chain(*number_indices)) if isinstance(x, tuple)
        ]
        digit_indices = [x for x in list(chain(*digit_indices)) if isinstance(x, tuple)]

        if digit_indices:
            first_digit_idx = min([min(x) for x in digit_indices])
            last_digit_idx = max([min(x) for x in digit_indices])
            first_digit = int(line[first_digit_idx])
            last_digit = int(line[last_digit_idx])

        if number_indices:
            first_number_idx = min([x for x in number_indices])
            last_number_idx = max([x for x in number_indices])
            first_number_str = line[first_number_idx[0] : first_number_idx[-1]]
            last_number_str = line[last_number_idx[0] : last_number_idx[-1]]
            first_number = NUMBERS[first_number_str]
            last_number = NUMBERS[last_number_str]

        if digit_indices and not number_indices:
            return first_digit, last_digit

        elif number_indices and not digit_indices:
            return first_number, last_number

        if min(digit_indices) < min(number_indices):
            first_val = first_digit
        else:
            first_val = first_number

        if max(digit_indices) > max(number_indices):
            last_val = last_digit
        else:
            last_val = last_number

        return first_val, last_val

    def solve(self) -> int:
        sum_nums = 0
        for line in s.data:
            first_num, last_num = s.find_first_and_last_number(line)
            sum_nums += int(f"{first_num}{last_num}")

        return sum_nums


if __name__ == "__main__":
    s = Solution()
    s.aocd.submit_puzzle(s.solve())
