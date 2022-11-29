import itertools
import pathlib
import time

from classes.template import AOCD

class Puzzle:
    def __init__(self):
        self.puzzle = AOCD()
        self.data_path = f"{pathlib.PurePath(__file__).stem}.txt"
        if not pathlib.Path(self.data_path).exists():
            self.save_puzzle(self.get_puzzle())
        with open(self.data_path, "r") as f:
            self.puzzle_data = f.read()

    def get_puzzle(self):
        return self.puzzle.data

    def save_puzzle(self, data):
        with open(self.data_path, "w") as f:
            f.write(data)

class Part_A:
    def __init__(self):
        self.puzzle_data = Puzzle().puzzle_data

    def count(self):
        puzzle = list(self.puzzle_data)
        return puzzle.count("(") - puzzle.count(")")

class Part_B():
    def __init__(self):
        self.puzzle_data = Puzzle().puzzle_data
        
    def count(self):
        time_start = time.time()
        instruction_map = str.maketrans(
            {
                "(": "1",
                ")": "-1"
            }
        )
        instructions = list(self.puzzle_data)
        instructions = [int(x) for x in ",".join(instructions).translate(instruction_map).split(",")]
        instruction_count = list(itertools.takewhile(lambda x: x >= 0, itertools.accumulate(instructions)))
        time_stop = time.time()
        return len(instruction_count) + 1, (time_stop - time_start)

    def count_2(self):
        time_start = time.time()
        count = 0 
        for instruction_count, x in enumerate(list(self.puzzle_data), start=1):
            if x == "(":
                count += 1
            elif x == ")":
                count -= 1
            if count < 0:
                break
        time_stop = time.time()
        return instruction_count, (time_stop - time_start)

if __name__ == "__main__":
    part_a = Part_A()
    part_b = Part_B()
    puzzle = Puzzle()
    try:
        puzzle.puzzle.submit_puzzle(part_a.count())
    except puzzle.aocd.exceptions.AocdError as e:
        print(e.message)
    #puzzle.puzzle.submit_puzzle(part_b.count())
