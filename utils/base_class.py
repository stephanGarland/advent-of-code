import pathlib
from abc import ABC, abstractmethod
from typing import List

import aocd


class AOCD:
    def __init__(self, file_path):
        self.file_path = file_path
        self.calling_file = pathlib.PurePath(self.file_path)
        self.text_file = f"{self.calling_file.with_stem(self.calling_file.stem.rstrip('ab_')).stem}.txt"
        if not (
            pathlib.Path(self.text_file).is_file()
            and pathlib.Path(self.text_file).stat().st_size
        ):
            self.save_puzzle(self.download_puzzle())
        self.puzzle = self.get_puzzle()
        self.year, self.day = [
            int(x.rstrip(".py")) for x in self.calling_file.parts[-2:]
        ]

    def download_puzzle(self):
        return aocd.get_data(year=self.year, day=self.day)

    def get_puzzle(self):
        with open(self.text_file, "r") as f:
            self.puzzle = f.read().splitlines()
        return self.puzzle

    def save_puzzle(self, data):
        with open(self.text_file, "w") as f:
            f.write(data)

    def submit_puzzle(self, answer, year=None, day=None, part=None):
        return aocd.submit(
            answer=answer, year=year or self.year, day=day or self.day, part=part
        )


class AbstractAOCD(ABC):
    """Template for any Advent of Code solution."""

    def __init__(self, file_path):
        self.aocd = AOCD(file_path=file_path)

    @abstractmethod
    def parse_input(self, raw_input: List[str]):
        """Define how to parse the day's specific input format."""
        pass

    @abstractmethod
    def solve(self):
        """Define the solution logic for this part."""
        pass

    def _debug(self):
        try:
            with open("example.txt", "r") as f:
                self.puzzle = f.read().splitlines()
                self.data = self.parse_input(self.puzzle)
        except FileNotFoundError:
            print("ERROR: expected to find example.txt")
            raise

