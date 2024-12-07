import argparse
import importlib.util
import inspect
import pathlib
import sys
from datetime import datetime
from typing import Callable, List, Optional


def get_solution(
    day: Optional[int] = None, year: Optional[int] = None
) -> Optional[str]:
    """
    Find a specific solution file or the latest one with any implementation.

    Args:
        day: Optional day number (1-25)
        year: Optional year (defaults to current year)

    Returns:
        Path to the solution file
    """
    if year is None:
        year = datetime.now().year

    year_dir = pathlib.Path(f"{year}")
    if not year_dir.exists():
        raise FileNotFoundError(f"No solutions directory found for year {year}")

    if day is not None:
        if not (1 <= day <= 25):
            raise ValueError(f"Day must be between 1 and 25, got {day}")

        file_path = year_dir / f"{day:02d}.py"
        if not file_path.exists():
            raise FileNotFoundError(f"No solution file found for day {day}")

        return file_path

    for day in range(25, 0, -1):
        file_path = year_dir / f"{day:02d}.py"
        if not file_path.exists():
            continue

        spec = importlib.util.spec_from_file_location("solution", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        has_implementation = False
        for part in [module.PartOne, module.PartTwo]:
            source = inspect.getsource(part.solve)
            if "pass" not in source or len(source.strip().split("\n")[1:]) > 1:
                has_implementation = True
                break

        if has_implementation:
            return file_path

    raise FileNotFoundError(f"No implemented solutions found for year {year}")


def run_solution():
    """
    Command-line interface for running solutions.
    Usage: run_solution.py [--year YYYY] [--day DD] [solution args...]
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year", "-Y", type=int, help="Year to run (default: current year)"
    )
    parser.add_argument(
        "--day", "-d", type=int, help="Day to run (default: latest implemented)"
    )

    args, remaining_args = parser.parse_known_args()

    try:
        solution_path = get_solution(args.day, args.year)
        print(f"Running solution: {solution_path}", file=sys.stderr)
        sys.argv = [str(solution_path)] + remaining_args
        with open(solution_path) as f:
            exec(f.read())
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    run_solution()
