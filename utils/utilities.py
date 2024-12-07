import argparse
from collections import deque
import inspect
import itertools
from typing import Any, Generator, List, Optional, Sequence, Union


def print_or_submit_solution(
    part_a_cls, part_b_cls, file_path, part=None, submit=False, debug=False
) -> None:
    """
    Determines which solution to run based on implementation status and arguments.

    Args:
        part_a_cls: The PartA class
        part_b_cls: The PartB class
        file_path: Path to the solution file
        part: Optional part number [1, 2] to selectively run a specific part
        submit: If true, submits the solution
    """

    def is_implemented(cls):
        source = inspect.getsource(cls.solve)
        return "pass" not in source or len(source.strip().split("\n")[1:]) > 1

    part_a = part_a_cls(file_path)
    part_b = part_b_cls(file_path)

    if part is None:
        if is_implemented(part_b_cls):
            solution = part_b
            part = "b"
        elif is_implemented(part_a_cls):
            solution = part_a
            part = "a"
        else:
            raise NotImplementedError("No solution implemented yet!")
    elif part == "a":
        solution = part_a
    elif part == "b":
        solution = part_b

    if debug:
        solution._debug()
    result = solution.solve()

    if submit:
        solution.aocd.submit_puzzle(answer=result, part=part)
        print(f"Submitted solution for {solution.__class__.__name__}: {result}")
    else:
        print(f"Solution for {solution.__class__.__name__}: {result}")
        print("(use --submit to submit this solution)")


def find_first_unique_window(
    datastream, window_size: int, inclusive: bool = False
) -> Optional[int]:
    for i, window in enumerate(datastream):
        if len(set(window)) == window_size:
            if inclusive:
                return i + window_size
            return i
    return None


def is_ordered_subset(seq: Sequence, subseq: Sequence) -> bool:
    main_iter = iter(seq)
    return all(x in main_iter for x in subseq)

# https://stackoverflow.com/a/22045226/4221094
def make_groups(iterator, group_size: int) -> list[tuple]:
    it = iter(iterator)
    return list(iter(lambda: tuple(itertools.islice(it, group_size)), ()))


def parse_args():
    """Parse command line arguments for Advent of Code solutions."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Load example.txt from CWD"
    )
    parser.add_argument(
        "--part",
        choices=["a", "b"],
        help="Specify which part to run (default: latest implemented)",
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Submit the solution (default: just print)",
    )
    return parser.parse_args()


def sort_columns_pairwise(cols: List[List[int]]) -> List[List[int]]:
    """Sorts a 2D list, returning the same shape as given.
    Assuming input like: [[9, 5], [1, 3], [4, 0]], this will:
        * Transpose the list to: [[9, 1, 4], [5, 3, 0]]
        * Sort the list to: [[1, 4, 9], [0, 3, 5]]
        * Transpose and return the list as: [[1, 0], [4, 3], [9, 5]]
    """
    return [[*x] for x in zip(*map(sorted, zip(*cols)))]

def sliding_window(iterable, n: int) -> Generator:
    "Collect data into overlapping fixed-length chunks or blocks."
    iterator = iter(iterable)
    window = deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)

def transpose_list(lst: List[List], join: bool = False) -> List[Any]:
    """Transposes a 2D list."""

    if join:
        return ["".join([*x]) for x in zip(*lst)]
    return [[*x] for x in zip(*lst)]
