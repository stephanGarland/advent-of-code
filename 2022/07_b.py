from bisect import bisect_left

from more_itertools import flatten

from anytree import Node
from classes.template import AOCD as Base


class AOCD(Base):
    pass


class Solution:
    """
    Given a terminal output listing directories prefixed with dir,
    and files prefixed with integers, find the smallest directory
    that would yield a total free space of 30_000_000 bytes,
    out of a total disk size of 70_000_000 bytes.
    Note that nested directories should be counted both individually
    and with their parent.
    """

    def __init__(self):
        self.aocd = AOCD(file_path=__file__)
        self.data = [x.split() if x else "" for x in self.aocd.puzzle]
        self.all_dirs = []

    def traverse_fs(self, data):
        self.fs = Node(
            "/",
            file_size=0,
            ls_line="",
            is_dir=True,
            is_file=False,
        )
        cwd = self.fs
        for line in data:
            if line[0] == "$":
                if line[1] == "cd":
                    if line[2] == "/":
                        cwd = self.fs
                    elif line[2] == "..":
                        cwd = cwd.parent
                    else:
                        for child in cwd.children:
                            if child.name == line[2]:
                                cwd = child

            # Directory
            if line[0].isalpha():
                Node(
                    line[1],
                    parent=cwd,
                    file_size=0,
                    is_dir=True,
                    is_file=False,
                )
            # File
            elif line[0].isnumeric():
                Node(
                    line[1],
                    parent=cwd,
                    file_size=line[0],
                    is_dir=False,
                    is_file=True,
                )

        return self.fs

    def get_tree(self, filesystem: Node) -> Node:
        return filesystem.descendants

    def get_root_size(self, filesystem: Node):
        file_sizes = sum([int(x.file_size) for x in filesystem.children if x.is_file])
        subdir_sizes = sum(
            [self.get_root_size(x) for x in filesystem.children if not x.is_file]
        )
        return file_sizes + subdir_sizes

    def get_sizes(self, filesystem: Node) -> int:
        """
        This is hardly a best practice; having the method
        both modify a class variable and also return a value.
        """
        file_sizes = [int(x.file_size) for x in filesystem.children if x.is_file]
        subdir_sizes = [self.get_sizes(x) for x in filesystem.children if not x.is_file]
        all_sizes = file_sizes + subdir_sizes
        self.all_dirs.extend([all_sizes])

        return sum(all_sizes)


if __name__ == "__main__":
    s = Solution()
    filesystem = s.traverse_fs(s.data)
    s.get_sizes(filesystem)
    s.fs.file_size = s.get_sizes(filesystem)
    total_space = 70_000_000
    needed_space = 30_000_000
    free_space = total_space - s.fs.file_size
    space_to_clear = needed_space - free_space

    all_dir_sizes = sorted(list(flatten(s.all_dirs)))
    foo = bisect_left(all_dir_sizes, space_to_clear)

    s.aocd.submit_puzzle(all_dir_sizes[foo])
