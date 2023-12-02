import more_itertools

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
NUMBER_MAX_LEN = max([len(x) for x in NUMBERS.keys()])


class AOCD(Base):
    pass


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

    def find_first_number(self, line: str) -> int:
        try:
            return int(line[0])
        except ValueError:
            pass
        window: list[tuple[str]] = more_itertools.sliding_window(line, NUMBER_MAX_LEN)
        for win in window:
            digit = [x for x in win if x.isdigit()]
            # smallest possible alpha number takes three chars
            if digit and win.index(digit[0]) < 3:
                return int(digit[0])
            bitmap = [x in "".join(win) for x in NUMBERS.keys()]
            number = [x for x in [a and b for a, b in zip(bitmap, NUMBERS.keys())] if x]
            try:
                if (digit and not number) or (
                    (digit and number) and (win.index(digit[0]) < win.index(number[0]))
                ):
                    return int(digit[0])
                elif number:
                    return NUMBERS[number[0]]
                else:
                    pass
                    print(f"found nothing: {''.join(win)}")
            except ValueError:
                breakpoint()

    def solve(self) -> int:
        sum_nums = 0
        for line in s.data:
            first_num = s.find_first_number(line)
            last_num = s.find_first_number(line[::-1])
            sum_nums += int(f"{first_num}{last_num}")

        return sum_nums


if __name__ == "__main__":
    s = Solution()
    print(s.solve())
