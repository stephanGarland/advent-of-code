from itertools import takewhile
from more_itertools import flatten

from classes.template import AOCD as Base
from classes.utilities import Utilities


class AOCD(Base):
    pass


class Solution:
    """
    Given a matrix of integers representing the height of trees in a grid,
    determine the number of trees that are visible from outside the grid.
    A tree is visible if all trees between itself and an edge are shorter
    than it.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        # self.data = [[int(y) for y in x] for x in self.aocd.puzzle]
        with open("08_example.txt", "r") as f:
            self.data = [[int(y) for y in x] for x in f.read().splitlines()]
        self.utilities = Utilities()

    def make_slices(
        self, coords: tuple, tree_matrix: list
    ) -> dict[str, list[list[int]]]:
        slices = {}
        row, col = coords
        top_slice = [tree[col] for tree in tree_matrix][:row]
        bottom_slice = [tree[col] for tree in tree_matrix][row + 1 :]
        left_slice = tree_matrix[row][:col]
        right_slice = tree_matrix[row][col + 1 :]
        return {
            "top": top_slice,
            "bottom": bottom_slice,
            "left": left_slice,
            "right": right_slice,
        }

    def get_tree_slice(self, tree_matrix: list):
        visible = []
        grid_length = len(tree_matrix) - 1
        for row in range(grid_length):
            if row in [0, grid_length]:
                continue
            for col in range(grid_length):
                if col in [0, grid_length]:
                    continue
                coords = (row, col)
                tree_slices = self.make_slices(coords, tree_matrix)
                # tree_is_visible = all(tree_matrix[coords[0]][coords[1]] > tree for tree in )
                print(
                    f"row: {tree_matrix[row]}\t visible: {[(k, v) for k,v in tree_slices.items()]}"
                )
                visible_trees = self.find_visible(coords, tree_matrix, tree_slices)
                visible.append(visible_trees)

        return visible

    def find_visible(
        self, coords: tuple, tree_matrix: list, tree_slices: dict[str, list[list[int]]]
    ):
        visible = 0
        for trees in tree_slices.values():
            if all(tree_matrix[coords[0]][coords[1]] > tree for tree in trees):
                visible += 1
            # visible.append(
            #    len(list(takewhile(lambda x: x < tree_matrix[coords[0]][coords[1]], v)))
            # )
        return visible

    def solve(self):
        return len(self.get_tree_slice(tree_matrix))


if __name__ == "__main__":
    s = Solution()
    tree_matrix = s.data
    visible = s.get_tree_slice(tree_matrix)
    # for row in tree_matrix:
    #    print(row)
    # print(s.solve())
