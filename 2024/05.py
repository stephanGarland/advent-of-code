from collections import defaultdict
from graphlib import TopologicalSorter
from typing import Dict, List, NamedTuple, Set, Tuple

from utils import utilities
from utils.base_class import AbstractAOCD


class Data(NamedTuple):
    ordering: List[Tuple[int, ...]]
    updates: List[Tuple[int, ...]]


class PartA(AbstractAOCD):
    """
    Given a list of ordering for updates, e.g. 47|53, along with
    a list of pages to be updated, e.g. 75,47,61,53,29,
    determine if each each page update is correct or not. In the
    above simplistic example, 47 must update before 53, and it is.

    If there are any missing numbers in the ordering, instances of
    those numbers may be ignored in the update instructions.

    What is the sum of the middle number in every list of correct
    instructions?
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.data: Data = self.parse_input(self.aocd.puzzle)

    def parse_input(self, raw_data: List[str]) -> Data:
        sep = raw_data.index("")
        ordering: List[Tuple[int, ...]] = [
            tuple(int(item) for item in x.replace("|", " ").split())
            for x in raw_data[:sep]
        ]
        updates: List[Tuple[int, ...]] = [
            tuple(map(int, (x.split(",")))) for x in raw_data[sep + 1 :]
        ]

        return Data(ordering=ordering, updates=updates)

    def make_graph(self, update: Tuple[int, ...]) -> Dict[int, Set[int]]:
        graph = defaultdict(set)
        for rule in self.data.ordering:
            if set(rule).issubset(update):
                if rule[1] not in graph:
                    graph[rule[1]].add(rule[0])
                else:
                    graph[rule[1]].update(graph[rule[1]].union([rule[0]]))

        return graph

    def make_topo(self, graph: Dict[int, Set[int]]) -> Tuple[int, ...]:
        ts = TopologicalSorter(graph)

        return tuple(ts.static_order())

    def solve(self) -> int:
        middle_nums: List[int] = []
        for update in self.data.updates:
            graph: Dict[int, Set[int]] = self.make_graph(update)
            topo: Tuple[int, ...] = self.make_topo(graph)

            if utilities.is_ordered_subset(topo, update):
                middle_nums.append(update[len(update) // 2])

        return sum(middle_nums)


class PartB(PartA):
    """
    Fix the ordering of any incorrectly-ordered update instructions.
    What is the sum of these now-correctly ordered update instructions?
    """

    def solve(self) -> int:
        middle_nums: List[int] = []
        for update in self.data.updates:
            graph: Dict[int, Set[int]] = self.make_graph(update)
            topo: Tuple[int, ...] = self.make_topo(graph)

            if not utilities.is_ordered_subset(topo, update):
                middle_nums.append(topo[len(topo) // 2])

        return sum(middle_nums)


if __name__ == "__main__":
    args = utilities.parse_args()
    utilities.print_or_submit_solution(
        PartA, PartB, __file__, args.part, args.submit, args.debug
    )
