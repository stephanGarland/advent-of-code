#!/usr/bin/env python3
import argparse
import datetime
import logging
import os
import pathlib
from shutil import which
from sys import version_info

import aocd

"""
This bootstraps a new AoC directory structure.
Specifically, it can:
  * Template out some basic starter code, which exposes a day's input as
    a list of strings
  * Download your unique user's inputs for a given year range

It attempts to have some safety checking while doing the above, and will not,
for instance, clobber your existing work if you tell it to create new template
files. It also checks to see if you have any kind of VCS installed, and if not,
refuses to do anything without being forced.

TODO:
  * This relies on aocd's rate-limiting, which is less than ideal.
    I'd like to insert a manual sleep IFF aocd did _not_ find a cached file,
    but AFAICT that isn't exposed other than logging statements.
    Trying to hook into its log handler proved more trouble than it was worth.
"""


class Template:
    def __init__(self):
        self.args = self.make_args()
        self.working_dir = "".join(
            [f"{x}/" for x in pathlib.Path.cwd().parts if not x.isdigit()]
        ).replace("//", "/")
        if not self.prerequisites_are_met():
            raise SystemExit(1)

    def prerequisites_are_met(self):
        vcs_list = [".bzr", "CVS", ".git", ".hg", ".svn"]
        if not (
            os.environ.get("AOC_SESSION")
            or pathlib.Path(f"{str(pathlib.Path.home())}/.config/aocd/token").exists()
            or self.args.aocd_dir
        ):
            logging.fatal(
                "AOC session cookie or token not found, please set it as an env var or use --aoc-token"
            )
            return False
        if version_info.major < 3 or version_info.minor < 6:
            logging.fatal("Python version doesn't support f-strings, update to >= 3.6")
            return False

        if not any(
            [
                pathlib.Path(pathlib.PurePath(self.working_dir).joinpath(vcs)).is_dir()
                for vcs in vcs_list
            ]
        ):
            if self.args.vcs:
                logging.warning("--making-poor-decisions flag used")
                try:
                    with open("art.txt", "r") as f:
                        an_art = f"\033[91m{f.read()}\033[0m"
                    print(an_art)
                except FileNotFoundError:
                    pass
            else:
                logging.fatal(
                    "no revision control system found in PATH - use --making-poor-decisions to ignore"
                )
                return False
        return True

    def make_args(self):
        parser = argparse.ArgumentParser(description="Various functions for AoC")
        parser.add_argument(
            "-a",
            "--aocd-dir",
            dest="aocd_dir",
            help="Alternate path to AoC token directory",
        )
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
            "--making-poor-decisions",
            action="store_true",
            dest="vcs",
            help="Disregard best practices and allow overwriting with no VCS",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Set log level to DEBUG",
        )
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="Set log level to FATAL",
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
from classes.utilities import Utilities


class AOCD(Base):
    pass


class Solution:
    \"\"\"
    Foobar
    \"\"\"

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x for x in self.aocd.puzzle]
        self.utilities = Utilities()


if __name__ == "__main__":
    s = Solution()
"""

        return template

    def write_template(self, year_from, year_to):
        template = self.make_template()
        overwrote = False
        counter = 0
        for year in range(year_from, year_to + 1):
            for day in range(1, 26):
                for letter in ["a", "b"]:
                    py_path = pathlib.Path(
                        f"{self.working_dir}/{year}/{day:02d}_{letter}.py"
                    )
                    py_path.parent.mkdir(parents=True, exist_ok=True)
                    if py_path.exists():
                        with open(py_path, "r") as f:
                            if f.read() == template:
                                logging.debug(
                                    f"{py_path} exists and matches template, skipping"
                                )
                            elif not self.args.force:
                                logging.debug(f"{py_path} exists, skipping")
                                continue
                            else:
                                overwrote = True
                                logging.warning(f"{py_path} exists, overwriting")
                                counter += 1
                    else:
                        logging.debug(f"{py_path} not found, writing new file")
                    with open(py_path, "w+") as f:
                        f.write(template)

        if overwrote and self.args.force and self.args.quiet:
            if self.args.vcs:
                print(
                    f"\nATTENTION: {counter} files overwritten, with no version control. "
                    "git gud (is what you could use if you had version control)\n"
                )
            else:
                print(
                    f"\nATTENTION: {counter} files overwritten. If you need to roll some of them back, "
                    "shell parameter expansion works well.\ne.g. git restore "
                    "../2022/{{01..07}}_{{a,b}}.py to restore 2022/01_a.py - 2022/07_b.py\n"
                )

    def download_inputs(
        self, year_from: int, year_to: int
    ) -> dict[tuple[int, int], str]:
        input_dict = {}
        cur_date = datetime.datetime.now().date()
        for year in range(year_from, year_to + 1):
            for day in range(1, 26):
                if (
                    datetime.datetime.strptime(f"{year}-12-{day}", "%Y-%m-%d").date()
                    > cur_date
                ):
                    logging.debug("reached end of available puzzles, quitting early")
                    return input_dict
                day_path = pathlib.Path(f"{self.working_dir}/{year}/{day:02d}.txt")
                if not day_path.exists():
                    logging.debug(f"{day_path} not found, downloading new file")
                    try:
                        input_dict[(year, day)] = aocd.get_data(day=day, year=year)
                    except aocd.exceptions.PuzzleLockedError:
                        logging.error(f"{day_path} puzzle is not yet available")
                else:
                    logging.debug(f"{day_path} exists, skipping")

        return input_dict

    def write_inputs(self, input_dict: dict[tuple[int, int], str]):
        for k, v in input_dict.items():
            day_path = pathlib.Path(f"{self.working_dir}/{k[0]}/{k[1]:02d}.txt")
            day_path.parent.mkdir(parents=True, exist_ok=True)
            # TODO: determine if this and download_inputs should both do conflict checks
            if day_path.exists():
                with open(day_path, "r") as f:
                    if f.read() == v:
                        logging.debug(
                            f"{day_path} exists and matches downloaded, skipping"
                        )
                        continue
                    elif not self.args.force:
                        logging.debug(f"{day_path} exists, skipping")
                        continue
                    else:
                        logging.warning(f"{day_path} exists, overwriting")
            else:
                logging.debug(f"{day_path} not found, writing new file")
            with open(day_path, "w+") as f:
                f.write(v)


if __name__ == "__main__":
    t = Template()
    if t.args.quiet:
        log_level = logging.FATAL
    elif t.args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=log_level
    )
    if t.args.aocd_dir:
        os.environ["AOCD_DIR"] = t.args.aocd_dir
        print(os.environ["AOCD_DIR"])
    if t.args.download or t.args.template:
        if not (t.args.from_year or t.args.to_year):
            logging.fatal("year range not provided")
            raise SystemExit(1)
        elif t.args.from_year and not t.args.to_year:
            t.args.to_year = t.args.from_year
        elif t.args.to_year and not t.args.from_year:
            t.args.from_year = t.args.to_year
        if t.args.to_year < t.args.from_year:
            logging.fatal(
                f"invalid year range: to_year ({t.args.to_year}) < from_year ({t.args.from_year})"
            )
            raise SystemExit(1)
    if t.args.download:
        input_files = t.download_inputs(t.args.from_year, t.args.to_year)
        t.write_inputs(input_files)
    if t.args.template:
        t.write_template(t.args.from_year, t.args.to_year)
