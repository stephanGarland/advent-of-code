import collections
import copy
import itertools
import logging
import re
import string

from importlib import import_module

PartOne = import_module("05_a", "Solution")

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
    at the end. Note that the crane now moves multiple crates at a time.
    """

    def __init__(self):
        self.part_one = PartOne.Solution()
        self.aocd = AOCD(file_path=__file__)
        self.data = [x if x else "" for x in self.aocd.puzzle]
        self.logger = logging.getLogger("logger")
        logging.basicConfig(format=LOG_FORMAT)
        if DEBUG:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.utilities = Utilities()

    def get_crates(self, stacks: dict, stack: str, num_crates: str):
        crates = collections.deque()
        for _ in range(int(num_crates)):
            crate = stacks[stack].popleft()
            while crate not in string.ascii_uppercase:
                crate = stacks[stack].popleft()
            crates.appendleft(crate)

        return crates

    def perform_moves(self, moves: list[tuple], stacks: dict):
        """
        moves: list of tuples containing moves of the form
        <quantity_to_move>, <from_stack>, <to_stack>.
        stacks: dict of deques, with the key being the stack number.
        """

        for move in moves:
            self.logger.debug(f"retrieving {move[0]} crates from stack {move[1]}")
            old_stacks = copy.deepcopy(stacks)
            self.logger.debug(f"stack {move[1]} before move: {stacks[move[1]]}")
            crates_to_move = self.get_crates(stacks, move[1], move[0])
            self.logger.debug(f"inserting crates {crates_to_move} into stack {move[2]}")
            self.logger.debug(f"stack {move[1]} after move: {stacks[move[1]]}")
            for crate in crates_to_move:
                stacks[move[2]].appendleft(crate)
            self.part_one.debug_visualize(move, old_stacks, stacks)


if __name__ == "__main__":
    s = Solution()
    inputs = s.part_one.parse_input()
    stacks = s.part_one.make_starting_stacks(inputs[0])
    moves = re.findall(r"\d+", ",".join(inputs[1]))
    move_chunks = s.utilities.make_groups(moves, 3)
    s.perform_moves(move_chunks, stacks)
    final_stack = s.part_one.make_final_stack_report(stacks, [])
    answer = s.part_one.solve(final_stack)
    s.logger.info(f"*** GUESS: {answer} ***")
    s.aocd.submit_puzzle(answer)
