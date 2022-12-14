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
        self.data = [[int(y) for y in x] for x in self.aocd.puzzle]
        self.utilities = Utilities()

    def make_slices(
        self, coords: tuple, tree_matrix: list
    ) -> dict[str, list[list[int]]]:
        slices = {}
        row, col = coords
        top_slice = [int(tree[col]) for tree in tree_matrix][:row]
        bottom_slice = [int(tree[col]) for tree in tree_matrix][row + 1 :]
        left_slice = [int(x) for x in tree_matrix[row][:col]]
        right_slice = [int(x) for x in tree_matrix[row][col + 1 :]]
        return {
            "top": top_slice,
            "bottom": bottom_slice,
            "left": left_slice,
            "right": right_slice,
        }

    def loop_all_trees(self, tree_matrix: list) -> list:
        visible = []
        # Subtracting 1 since we're iterating over a 0-indexed range
        grid_length = len(tree_matrix) - 1
        for row in range(grid_length):
            if row in [0, grid_length]:
                continue
            for col in range(grid_length):
                if col in [0, grid_length]:
                    continue
                coords = (row, col)
                tree_slices = self.make_slices(coords, tree_matrix)
                visible_trees = self.find_visible(coords, tree_matrix, tree_slices)
                visible.append(visible_trees)

        return visible

    def find_visible(
        self, coords: tuple, tree_matrix: list, tree_slices: dict[str, list[list[int]]]
    ) -> bool:
        for direction, trees in tree_slices.items():
            all_visible = all(
                tree_matrix[coords[0]][coords[1]] > tree for tree in trees
            )
            # print(f"tree {coords} ({tree_matrix[coords[0]][coords[1]]}) in {tree_matrix[coords[0]]} against {trees} (direction {direction}): {all_visible}")
            if all_visible:
                return True
        return False

    def solve(self, tree_matrix: list) -> int:
        # Add the always visible trees on the perimeter, less the four duplicated corner trees
        perimeter_addition = (2 * (2 * len(s.data))) - 4
        return (
            len([x for x in self.loop_all_trees(tree_matrix) if x]) + perimeter_addition
        )


if __name__ == "__main__":
    s = Solution()
    tree_matrix = s.data
    s.aocd.submit_puzzle(s.solve(tree_matrix))
