from math import prod
from more_itertools import seekable

from classes.template import AOCD as Base
from classes.utilities import Utilities


class AOCD(Base):
    pass


class Solution:
    """
    Given a matrix of integers representing the height of trees in a grid,
    determine the highest scenic score for any tree in the grid, where the
    scenic score is equal to the product of the number of trees visible
    from each tree in each cardinal direction. For example, if a given tree
    of height five can see 1 tree to its left and right, 2 trees to its
    bottom, and 3 trees to its top, its score would be (1 * 1 * 2 * 3) == 6.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x for x in self.aocd.puzzle]
        self.utilities = Utilities()

    def make_slices(
        self, coords: tuple, tree_matrix: list
    ) -> dict[str, list[list[int]]]:
        slices = {}
        row, col = coords
        top_slice = [int(tree[col]) for tree in tree_matrix][:row][::-1]
        bottom_slice = [int(tree[col]) for tree in tree_matrix][row + 1 :]
        left_slice = [int(x) for x in tree_matrix[row][:col]][::-1]
        right_slice = [int(x) for x in tree_matrix[row][col + 1 :]]
        return {
            "top": top_slice,
            "bottom": bottom_slice,
            "left": left_slice,
            "right": right_slice,
        }

    def loop_all_trees(self, tree_matrix: list) -> list:
        visible = []
        grid_length = len(tree_matrix)
        for row in range(grid_length):
            if row in [0, grid_length - 1]:
                continue
            for col in range(grid_length):
                if col in [0, grid_length - 1]:
                    continue
                coords = (row, col)
                tree_slices = self.make_slices(coords, tree_matrix)
                visible_trees = self.find_visible(coords, tree_matrix, tree_slices)
                visible.append(visible_trees)
        return visible

    def find_visible(
        self, coords: tuple, tree_matrix: list, tree_slices: dict[str, list[list[int]]]
    ) -> int:
        visible = []
        target_tree = int(tree_matrix[coords[0]][coords[1]])
        for direction, trees in tree_slices.items():
            visible_trees = 0
            it = seekable(trees)
            while bool(it):
                current_tree = next(it)
                if current_tree < target_tree:
                    visible_trees += 1
                else:
                    visible_trees += 1
                    break
            visible.append(visible_trees)
        return visible

    def solve(self, tree_matrix: list) -> int:
        grid_length = len(tree_matrix)
        visible = self.loop_all_trees(tree_matrix)
        return visible


if __name__ == "__main__":
    s = Solution()
    tree_matrix = s.data
    scores = s.solve(tree_matrix)
    answer = max([prod(row) for row in scores])
    s.aocd.submit_puzzle(answer)

