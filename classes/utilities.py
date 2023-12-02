import itertools
import more_itertools


class Utilities:
    # https://stackoverflow.com/a/22045226/4221094
    def make_groups(self, iterator, group_size: int) -> list[tuple]:
        it = iter(iterator)
        return list(iter(lambda: tuple(itertools.islice(it, group_size)), ()))

    def find_first_unique_window(
        self, datastream, window_size: int, inclusive: bool = False
    ) -> int:
        for i, window in enumerate(datastream):
            if len(set(window)) == window_size:
                if inclusive:
                    return i + window_size
                return i
