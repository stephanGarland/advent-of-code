import collections
import itertools
import operator
import pathlib

from classes.template import AOCD as Base
from classes.utilities import Utilities


class AOCD(Base):
    pass


class Solution:
    """
    Given a terminal output listing directories prefixed with dir,
    and files prefixed with integers, find the sum size of all
    directories having a total size < = 100000. Note that nested
    directories should be counted both individually and with their parent.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x.split() if x else "" for x in self.aocd.puzzle]
        self.utilities = Utilities()

    # https://gist.github.com/hrldcpr/2012250
    def tree(self):
        """
        Creates an autovivifying tree out of defaultdicts
        """

        return collections.defaultdict(self.tree)

    def traverse_fs(self, data):
        """
        Iterates over the input, and for cd, appends '/'-delimited directories
        to a list to build the absolute path. If the directory goes up one level
        with '..', the last item of the list is deleted.

        ls is skipped, because nothing needs to be done except read the next output.

        If an entry is an alpha, it's a directory name, so it's added to the tree.
        If an entry is numeric, it's a file's size, so both the name and size are
        added to the tree.

        Example output, after being prettied up with this helper function,
        then pretty-printed:

        def print_tree(t):
            return {k: print_tree(t[k]) for k in t}

        pprint.pprint(print_tree(fs), width=60)
        {'/': {'a': {},
               'b.txt': {'14848514': {}},
               'c.dat': {'8504156': {}},
               'd': {}},
         '/a/': {'e': {},
                 'f': {'29116': {}},
                 'g': {'2557': {}},
                 'h.lst': {'62596': {}}},
         '/a/e/': {'i': {'584': {}}},
         '/d/': {'d.ext': {'5626152': {}},
                 'd.log': {'8033020': {}},
                 'j': {'4060174': {}},
                 'k': {'7214296': {}}}}
        """
        fs = self.tree()
        cwd = []
        for line in data:
            if line[0] == "$":
                # Since the commands only change dir by depth=1
                # the cwd can be built in this way
                if line[1] == "cd":
                    if line[2] == "/":
                        cwd.append("/")
                    elif line[2] == "..":
                        del cwd[-1]
                    else:
                        cwd.append(f"{line[2]}/")
                elif line[1] == "ls":
                    continue
            # Directory
            if line[0].isalpha():
                fs["".join([f"{x}" for x in cwd])][line[1]]
            # File
            elif line[0].isnumeric():
                fs["".join([f"{x}" for x in cwd])][line[1]][line[0]]

        return fs

    def parse_fs(self, fs) -> dict[str, list[list[str]]]:
        """
        This takes the tree above and parses out the necessary information:
        the size of all files contained in a given directory. This is done by
        first making a 2D list with filenames and their size:

        [['a', ''], ['b.txt', '14848514'], ['c.dat', '8504156'], ['d', '']]
        [['e', ''], ['f', '29116'], ['g', '2557'], ['h.lst', '62596']]
        [['i', '584']]
        [['j', '4060174'], ['d.log', '8033020'], ['d.ext', '5626152'], ['k', '7214296']]


        Then, the list is flattened, and the sizes are cast to an int if they're numeric.
        The resultant list of integers is then summed, and stored as the value for its key.
        """
        parsed_fs = {}
        for k, v in fs.items():
            dir_listings = [
                [file, "".join([x for x in v[file].keys()])] for file in v.keys()
            ]
            parsed_fs[k] = sum(
                [
                    int(x)
                    for x in itertools.chain.from_iterable(dir_listings)
                    if x.isnumeric()
                ]
            )

        return parsed_fs

    def make_candidate_dirs(self, parsed_fs):
        candidates = []
        for path, size in parsed_fs.items():
            if size <= 100_000:
                candidates.append(path)

        return candidates

    def check_for_duplication(self, candidates: list, parsed_fs: dict):
        parsed_fs["extra"] = 0
        for path_1, path_2 in itertools.permutations(candidates, 2):
            if pathlib.PurePath(path_1).is_relative_to(pathlib.PurePath(path_2)):
                parsed_fs["extra"] += parsed_fs[path_1]

    def solve(self, candidates: list, parsed_fs: dict):
        candidates.append("extra")
        return sum(operator.itemgetter(*candidates)(parsed_fs))


if __name__ == "__main__":
    s = Solution()
    filesystem = s.traverse_fs(s.data)
    parsed_fs = s.parse_fs(filesystem)
    candidates = s.make_candidate_dirs(parsed_fs)
    duplicates = s.check_for_duplication(candidates, parsed_fs)
    answer = s.solve(candidates, parsed_fs)
    s.aocd.submit_puzzle(answer)
