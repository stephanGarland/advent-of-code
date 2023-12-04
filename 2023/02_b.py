from importlib import import_module

PartOne = import_module("02_a", "Solution")


class Solution:
    """
    Given inputs of RGB cubes pulled from a bag, what is the minimum number
    of cubes to make that game possible? Find the product of the minimum
    number of RGB cubes for each game (e.g. 4[R] * 2[G] * 3[B] = 24).
    Return the sum of these products.
    """

    def __init__(self):
        self.part_one = PartOne.Solution()

    def game_product(self, game_data: list) -> int:
        red_needed, grn_needed, blu_needed = 0, 0, 0
        for rnd in game_data:
            red_needed = max(red_needed, rnd.get("red", 0))
            grn_needed = max(grn_needed, rnd.get("green", 0))
            blu_needed = max(blu_needed, rnd.get("blue", 0))
        return red_needed * grn_needed * blu_needed

    def solve(self, game: list):
        products = []
        products.append(self.game_product(self.part_one.game_parser(game)))
        return sum(products)


if __name__ == "__main__":
    s = Solution()
    products = []
    for game in s.part_one.data:
        parsed = s.part_one.game_parser(game)
        products.append(s.game_product(parsed))
    s.part_one.aocd.submit_puzzle(sum(products))
