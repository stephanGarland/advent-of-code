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

    def count(self):
        puzzle = list(self.puzzle_data)
        return puzzle.count("(") - puzzle.count(")")


if __name__ == "__main__":
    puzzle = Puzzle()
    solution = Solution()
    puzzle.puzzle.submit_puzzle(solution.count())
