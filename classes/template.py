import inspect
import pathlib

import aocd

class AOCD:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = aocd.data
        self.calling_file = pathlib.PurePath(self.file_path)
        self.text_file = f"{self.calling_file.with_stem(self.calling_file.stem.rstrip('ab_')).stem}.txt"

    def get_caller(self):
        self.frame = inspect.currentframe().f_back.f_back
        self.caller = self.frame.f_code
        self.filename = pathlib.PurePath(self.caller.co_filename)
        self.filename_base = self.filename.with_stem(self.filename.stem.rstrip("ab_"))
        return self.filename_base.stem

    def save_puzzle(self, data):
        with open(f"{self.get_caller()}.txt", "w") as f:
            f.write(self.data)

    def submit_puzzle(self, answer):
        return aocd.submit(answer)

