import itertools

class Utilities:

    # https://stackoverflow.com/a/22045226/4221094
    def make_group(self, iterator, group_size):
        it = iter(iterator)
        return list(iter(lambda: tuple(itertools.islice(it, group_size)), ()))

