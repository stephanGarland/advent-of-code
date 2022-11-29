
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
