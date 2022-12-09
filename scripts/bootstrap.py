#!/usr/bin/env python3

import argparse
import datetime
import logging
import os
import pathlib
from sys import version_info

import aocd

MAX_ALLOWED_CTIME_DELTA = 60


class Template:
    def __init__(self):
        self.args = self.make_args()
        self.parent_dir = pathlib.Path.cwd().parent
        prereqs = self.prerequisites_are_met()
        if not prereqs:
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
            "-v",
            "--verbose",
            action="store_true",
            help="Print debug messages",
        )
        parser.add_argument(
            "-t",
            "--template",
            action="store_true",
            help="Create starter template .py files",
        )
        parser.add_argument(
            "-y",
            "--from-year",
            dest="from_year",
            default=0,
            type=int,
            help="The year range start to use",
        )
        parser.add_argument(
            "-Y",
            "--to-year",
            dest="to_year",
            default=0,
            type=int,
            help="The year range end to use",
        )

        return parser.parse_args()

    def make_template(self):
        template = """from classes.template import AOCD as Base

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

    def write_template(self, year_from, year_to):
        template = self.make_template()
        for year in range(year_from, year_to + 1):
            for day in range(1, 26):
                for letter in ["a", "b"]:
                    py_path = pathlib.Path(
                        f"{self.parent_dir}/{year}/{day:02d}_{letter}.py"
                    )
                    py_path.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        py_path_ctime = datetime.datetime.fromtimestamp(
                            py_path.stat().st_ctime
                        )
                        py_path_ctime_delta = (
                            datetime.datetime.now() - py_path_ctime
                        ).seconds
                    except FileNotFoundError:
                        logging.debug(f"{py_path} not found, writing new file")
                        py_path_ctime_delta = 0
                    if py_path.exists() and not (
                        self.args.force
                        or py_path_ctime_delta <= MAX_ALLOWED_CTIME_DELTA
                    ):
                        logging.error(f"{py_path} exists, skipping")
                        continue
                    elif py_path.exists() and self.args.force:
                        logging.warning(f"{py_path} exists, overwriting")
                    with open(py_path, "w+") as f:
                        f.write(template)

    def download_inputs(
        self, year_from: int, year_to: int
    ) -> dict[tuple[str, str], str]:
        input_dict = {}
        for year in range(year_from, year_to + 1):
            for day in range(1, 26):
                day_path = pathlib.Path(f"{self.parent_dir}/{year}/{day:02d}.txt")
                if not day_path.exists():
                    logging.debug(f"{day_path} not found, downloading new file")
                    input_dict[(year, day)] = aocd.get_data(day=day, year=year)
                else:
                    logging.debug(f"{day_path} exists, skipping")

        return input_dict

    def write_inputs(self, input_dict: dict[tuple[str, str], str]):
        for k, v in input_dict.items():
            day_path = pathlib.Path(f"{self.parent_dir}/{k[0]}/{k[1]:02d}.txt")
            day_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                day_path_ctime = datetime.datetime.fromtimestamp(
                    day_path.stat().st_ctime
                )
                day_path_ctime_delta = (
                    datetime.datetime.now() - day_path_ctime
                ).seconds
            except FileNotFoundError:
                logging.debug(f"{day_path} not found, writing new file")
                day_path_ctime_delta = 0
            if day_path.exists() and not (
                self.args.force or day_path_ctime_delta <= MAX_ALLOWED_CTIME_DELTA
            ):
                logging.error(f"{day_path} exists, skipping")
                continue
            elif day_path.exists() and self.args.force:
                logging.warning(f"{day_path} exists, overwriting")
            with open(day_path, "w+") as f:
                f.write(v)


if __name__ == "__main__":
    t = Template()
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if t.args.verbose else logging.INFO,
    )
    if t.args.download or t.args.template:
        if not (t.args.from_year or t.args.to_year):
            logging.fatal("year range not provided")
            raise SystemExit(1)
        elif t.args.from_year and not t.args.to_year:
            t.args.to_year = t.args.from_year
        elif t.args.to_year and not t.args.from_year:
            t.args.from_year = t.args.to_year
        if t.args.to_year < t.args.from_year:
            logging.fatal(f"invalid year range: to_year ({t.args.to_year}) < from_year ({t.args.from_year})")
            raise SystemExit(1)
    if t.args.download:
        input_files = t.download_inputs(t.args.from_year, t.args.to_year)
        t.write_inputs(input_files)
    elif t.args.template:
        t.write_template(t.args.from_year, t.args.to_year)
