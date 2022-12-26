from math import hypot, sqrt
from operator import sub

from classes.template import AOCD as Base
from classes.utilities import Utilities

class AOCD(Base):
    pass


class Solution:
    """
    Given a list of space-separated vectors representing the position
    of the head of a rope, find the number of unique positions that
    the tail of the rope will land on, if the tail must follow the head
    any time the distance between the head and tail exceeds 1. The tail
    can move orthogonally or diagonally.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        with open("09_example.txt", "r") as f:
            self.data = [[int(y) if y.isdigit() else y for y in x if y.isalnum()] for x in f.read().splitlines()]
        #self.data = [x for x in self.aocd.puzzle]
        self.utilities = Utilities()
    
    def move(self, tup: tuple[int], direction: str) -> tuple[int]:
        if direction == "R":
            return (tup[0] + 1, tup[1])
        if direction == "L":
            return (tup[0] - 1, tup[1])
        if direction == "U":
            return (tup[0], tup[1] + 1)
        if direction == "D":
            return (tup[0], tup[1] - 1)

    def hypotenuse(self, head: tuple[int], tail: tuple[int]) -> float:
        return hypot(head[0] - tail[0], head[1] - tail[1])

    def make_grid(self):
        head = (0, 0)
        tail = (0, 0)
        grid = self.visualize()
        visited = set()
        visited.add(tail)
        for direction, magnitude in s.data:
            for _ in range(magnitude):
                input()
                head = self.move(head, direction)
                print(f"direction: {direction}")
                if abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
                    if self.hypotenuse(head, tail) <= sqrt(2):
                            print(f"head: {head}, tail: {tail}, hypotenuse: {self.hypotenuse(head, tail)}\n")
                            grid = self.visualize()
                            tail = self.move(tail, direction)
                            print(f"head: {head}, tail: {tail}, hypotenuse: {self.hypotenuse(head, tail)}\n")
                    else:
                        print(f"head: {head}, tail: {tail}, hypotenuse: {self.hypotenuse(head, tail)}\n")
                        if direction == "U":
                            grid = self.visualize()
                            tail = self.move(tail, "U")
                            tail = self.move(tail, "L")
                        elif direction == "D":
                            grid = self.visualize()
                            tail = self.move(tail, "D")
                            tail = self.move(tail, "R")
                        elif direction == "R":
                            grid = self.visualize()
                            tail = self.move(tail, "U")
                            tail = self.move(tail, "R")
                        elif direction == "L":
                            grid = self.visualize()
                            tail = self.move(tail, "L")
                            tail = self.move(tail, "D")
                        print(f"head: {head}, tail: {tail}, hypotenuse: {self.hypotenuse(head, tail)}\n")
                grid[head[0]][head[1]] = "H"
                grid[tail[0]][tail[1]] = "T"
                for row in reversed(grid):
                    print(row)
                visited.add(tail)
        return visited, grid

    def visualize(self):
        return [["."] * 10 for x in range(10)]

if __name__ == "__main__":
    s = Solution()
    visited, grid = s.make_grid()
    for row in reversed(grid):
        #print(row)
        pass
    #for v in s.make_grid():
    #    print(v)
    print(len(visited))
