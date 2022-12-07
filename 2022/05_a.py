import collections
import copy
import itertools
import logging
import re
import string

from classes.template import AOCD as Base
from classes.utilities import Utilities

LOG_FORMAT = "%(levelname)s - %(message)s"
DEBUG = False


class AOCD(Base):
    pass


class Solution:
    """
    Given an ASCII table of crate stacks 1-9, where each crate
    is represented with an uppercase letter, and newline-separated
    instructions for moving crates from one stack to another,
    determine the crate that will be at the top of each stack
    at the end.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x if x else "" for x in self.aocd.puzzle]
        self.logger = logging.getLogger("logger")
        logging.basicConfig(format=LOG_FORMAT)
        if DEBUG:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.utilities = Utilities()

    def parse_input(self) -> tuple[list[str], list[str]]:
        """
        Splits the input on an empty string, returning a 2D list.
        """
        input_index = self.data.index("")
        split_data = [self.data[:input_index], self.data[input_index + 1 :]]

        return split_data[0], split_data[1]

    def make_starting_stacks(self, stack_input: list) -> dict:
        """
        Returns a dict of deques, with the stack number as the key.
        """
        starting_stacks = {}
        filtered_stacks = [x.replace("[", " ").replace("]", " ") for x in stack_input]
        del filtered_stacks[-1]
        transposed_filtered_stacks = [
            [*x] for x in zip(*filtered_stacks) if any(c.isalpha() for c in x)
        ]
        for i, row in enumerate(transposed_filtered_stacks, start=1):
            starting_stacks[str(i)] = collections.deque(x for x in row)
        return starting_stacks

    def get_crate(self, stacks: dict, stack: str):
        """
        This was originally using recursion, the same as make_final_stack_report()
        However, a bug was encountered with empty deques, where after successfully
        recursing after experiencing empty results, the first non-empty was ignored.

        Original code is below:

        def get_crate(self, stacks: dict, move: str):
            crate = stacks[move[1]].popleft()
            if not crate in string.ascii_uppercase:
                self.logger.debug(f"{stacks[stack]} was empty, received {crate}, recursing")
                self.get_crate(stacks, move)
            return crate
        """

        crate = stacks[stack].popleft()
        while crate not in string.ascii_uppercase:
            self.logger.debug(f"{stacks[stack]} was empty, received {crate}, looping")
            crate = stacks[stack].popleft()
        return crate

    def perform_moves(self, moves: list[tuple], stacks: dict):
        """
        moves: list of tuples containing moves of the form
        <quantity_to_move>, <from_stack>, <to_stack>.
        stacks: dict of deques, with the key being the stack number.
        """
        for move in moves:
            for _ in range(int(move[0])):
                self.logger.debug(f"retrieving {move[0]} crates from stack {move[1]}")
                old_stacks = copy.deepcopy(stacks)
                self.logger.debug(f"stack {move[1]} before move: {stacks[move[1]]}")
                crate_to_move = self.get_crate(stacks, move[1])
                self.logger.debug(
                    f"inserting crate {crate_to_move} into stack {move[2]}"
                )
                self.logger.debug(f"stack {move[1]} after move: {stacks[move[1]]}")
                stacks[move[2]].appendleft(crate_to_move)
                self.debug_visualize(move, old_stacks, stacks)

    def make_final_stack_report(self, stacks: dict, final_stack: list):
        """
        Recursively gets the first crate from the deques.
        """
        for stack in stacks.values():
            while len(stack) > 0:
                crate = stack.popleft()
                if crate != "":
                    final_stack.append(crate)
                    stack.clear()
                    continue
                else:
                    self.make_final_stack_report(stacks, final_stack)

        return final_stack

    def debug_visualize(self, move, old_stacks, stacks):
        column_numbers = self.parse_input()[0][-1]
        self.logger.debug(f"{move}")
        self.logger.debug("*** START ***")
        for row in list(itertools.zip_longest(*old_stacks.values(), fillvalue=" ")):
            self.logger.debug(
                " ".join([f"[{x}]" if x.isalpha() else "[ ]" for x in row])
            )
        self.logger.debug(column_numbers)
        self.logger.debug("*** FINISH ***")
        for row in list(itertools.zip_longest(*stacks.values(), fillvalue=" ")):
            self.logger.debug(
                " ".join([f"[{x}]" if x.isalpha() else "[ ]" for x in row])
            )
        self.logger.debug(column_numbers)

    def solve(self, crates: list):
        return "".join(crates)


if __name__ == "__main__":
    s = Solution()
    inputs = s.parse_input()
    stacks = s.make_starting_stacks(inputs[0])
    moves = re.findall(r"\d+", ",".join(inputs[1]))
    move_chunks = s.utilities.make_group(moves, 3)
    s.perform_moves(move_chunks, stacks)
    final_stack = s.make_final_stack_report(stacks, [])
    s.logger.info(f"*** GUESS: {s.solve(final_stack)} ***")
    # This was manually extracted and calculated from the first 10 lines
    # s.logger.info(f"*** ANSWER: CZWQZDDSW ***")
    s.aocd.submit_puzzle(s.solve(final_stack))
