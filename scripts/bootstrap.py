#!/usr/bin/env python3

import argparse
import logging
import os
import pathlib
from sys import version_info


class Template:
    def __init__(self):
        self.args = self.make_args()
        if not self.prerequisites_are_met():
            raise SystemExit(1)

    def prerequisites_are_met(self):
        if not (
            os.environ.get("AOC_SESSION") or pathlib.Path("$HOME/.config/aocd/token")
        ):
            logging.fatal(
                "AOC session cookie not found - please set it with `export AOC_SESSION`"
            )
            return False
        if version_info.major < 3 or version_info.minor < 6:
            logging.fatal("Python version doesn't support f-strings, update to >= 3.6")
            return False
        try:
            import aocd
        except ImportError:
            logging.fatal("aocd library is missing, please install it")

        return True

    def make_args(self):
        parser = argparse.ArgumentParser(description="Various functions for AoC.")
        parser.add_argument(
            "-d",
            "--download",
            action="store_true",
            help="Download and write AoC input files",
        )
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Forcibly overwrite existing files",
        )
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="Suppress all non-error messages",
        )
        parser.add_argument(
            "-t",
            "--template",
            action="store_true",
            help="Create starter template .py files",
        )
        parser.add_argument(
            "-y", "--from-year", type=int, help="The year range start to use"
        )
        parser.add_argument(
            "-Y", "--to-year", type=int, help="The year range end to use"
        )

        return parser.parse_args()

    def make_template(self):
        template = """ 
        from classes.template import AOCD as Base


        class AOCD(Base):
            pass


        class Solution:
            \"\"\"

            \"\"\"

            def __init__(self):
                self.aocd = AOCD(file_path=__file__)
                self.data = [int(x) if x else "" for x in self.aocd.puzzle]
                self.utilities = Utilities()


        if __name__ == "__main__":
            s = Solution()

        """

        return template

    def write_template(self):
        template = self.make_template()
        for year in range(year_from, year_to + 1):
            for day in range(1, 26):
                for letter in ["a", "b"]:
                    py_path = pathlib.Path(f"{k[0]}/{k[1]:02d}.py")
                    if py_path.exists() and not self.args.force:
                        logging.error(f"{py_path} exists, skipping")
                        continue
                    elif py_path.exists() and self.args.force:
                        logging.info(f"{py_path} exists, overwriting")
                    with open(py_path, "w") as f:
                        f.write(template)

    def download_inputs(
        self, year_from: int, year_to: int
    ) -> dict[tuple[str, str], str]:
        input_dict = {}
        for year in range(year_from, year_to + 1):
            for day in range(1, 26):
                input_dict[(year, day)] = aocd.get_data(day=day, year=year)

        return input_dict

    def write_inputs(self, inputs: dict[tuple[str, str], str]):
        for k, v in input_dict.values():
            day_path = pathlib.Path(f"{k[0]}/{k[1]:02d}.txt")
            if day_path.exists() and not self.args.force:
                logging.error(f"{day_path} exists, skipping")
                continue
            elif day_path.exists() and self.args.force:
                logging.info(f"{day_path} exists, overwriting")
            with open(day_path, "w") as f:
                f.write(v)


if __name__ == "__main__":
    t = Template()
    if t.args.download:
        input_files = t.download_inputs(self.args.year_from, self.args.year_to)
        t.write_inputs(input_files)
    elif self.args.template:
        t.write_template()
