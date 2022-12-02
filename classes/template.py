import pathlib

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

    def download_puzzle(self):
        return aocd.data

    def get_puzzle(self):
        with open(self.text_file, "r") as f:
            self.puzzle = f.read().splitlines()
        return self.puzzle

    def save_puzzle(self, data):
        with open(self.text_file, "w") as f:
            f.write(data)

    def submit_puzzle(self, answer):
        return aocd.submit(answer)
