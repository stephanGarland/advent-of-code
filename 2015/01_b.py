import itertools
import pathlib

from classes.template import AOCD

class Puzzle:
    def __init__(self):
        self.puzzle = AOCD()
        self.data_path = f"{self.puzzle.get_caller()}.txt"
        if not pathlib.Path(self.data_path).exists():
            self.puzzle.save_puzzle(self.get_puzzle())
        with open(self.data_path, "r") as f:
            self.puzzle_data = f.read()

    def get_puzzle(self):
        return self.puzzle.data

class Solution:
    def __init__(self):
        self.puzzle_data = Puzzle().puzzle_data
    
    # This is an order of magnitude slower than count_2(), but was interesting to try
    def count(self):
        instruction_map = str.maketrans(
            {
                "(": "1",
                ")": "-1"
            }
        )
        instructions = list(self.puzzle_data)
        instructions = [int(x) for x in ",".join(instructions).translate(instruction_map).split(",")]
        instruction_count = list(itertools.takewhile(lambda x: x >= 0, itertools.accumulate(instructions)))
        return len(instruction_count) + 1

    def count_2(self):
        count = 0 
        for instruction_count, x in enumerate(list(self.puzzle_data), start=1):
            if x == "(":
                count += 1
            elif x == ")":
                count -= 1
            if count < 0:
                break
        return instruction_count

if __name__ == "__main__":
    puzzle = Puzzle()
    solution = Solution()
    puzzle.puzzle.submit_puzzle(solution.count())

