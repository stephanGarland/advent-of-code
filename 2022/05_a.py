import collections
import itertools
import re
import string

from classes.template import AOCD as Base
from classes.utilities import Utilities


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
        #with open("example.txt", "r") as f:
        #    self.data = [x if x else "" for x in f.read().splitlines()]
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
        transposed_filtered_stacks = [[*x] for x in zip(*filtered_stacks) if any(c.isalpha() for c in x)] 
        for i, row in enumerate(transposed_filtered_stacks, start=1):
            starting_stacks[str(i)] = collections.deque(x for x in row)
        return starting_stacks
     
    def get_crate(self, stacks: dict, move: str):
        try:
            crate = stacks[move[1]].popleft()
        except IndexError as e:
            # I feel like this is the issue - with a known input set and instructions,
            # this shouldn't be needed, since the crane shouldn't be moving more crates than exist.
            raise e
        if not crate in string.ascii_uppercase:
            self.get_crate(stacks, move)
        return crate

    def perform_moves(self, moves: list[tuple], stacks: dict):
        """
        moves: list of tuples containing moves of the form
        <quantity_to_move>, <from_stack>, <to_stack>.
        stacks: dict of deques, with the key being the stack number.
        """
        for move in moves:
            #input()
            for _ in range(int(move[0])):
                #crate_to_move = stacks[move[1]].popleft()
                crate_to_move = self.get_crate(stacks, move)
                #if crate_to_move is None:
                #    return
                stacks[move[2]].appendleft(crate_to_move)

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

    def debug_print(self, move, inputs, stacks):
        print(f"\n{move}\n")
        print("\n*** START ***")
        for row in inputs[0]:
            print(row)
        print("\n*** FINISH ***")
        for row in list(itertools.zip_longest(*stacks.values(), fillvalue=" ")):
            print(" ".join([f"[{x}]" if x.isalpha() else "[ ]" for x in row]))

    def solve(self, crates: list):
        return "".join(crates)

if __name__ == "__main__":
    s = Solution()
    inputs = s.parse_input()
    stacks = s.make_starting_stacks(inputs[0])
    moves = re.findall(r"\d+", ",".join(inputs[1]))
    move_chunks = s.utilities.make_group(moves, 3)
    s.perform_moves(move_chunks, stacks)
    #print("\n*** START ***")
    #for row in inputs[0]:
    #    print(row)
    #print("\n*** FINISH ***")
    #for row in list(itertools.zip_longest(*stacks.values(), fillvalue=" ")):
    #    print(" ".join([f"[{x}]" for x in row]))
    final_stack = s.make_final_stack_report(stacks, [])
    print(f"\n*** GUESS: {s.solve(final_stack)} ***")

    #s.aocd.submit_puzzle(s.solve(final_stack))
