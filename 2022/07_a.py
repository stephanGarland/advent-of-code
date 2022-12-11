import datetime
import random

from anytree import Node, render, search

from classes.template import AOCD as Base
from classes.utilities import Utilities


class AOCD(Base):
    pass


class Inode:
    """
    Little reason to have this, but I needed some way to uniquely
    identify path stems, and I'm already committed to the fake filesystem.
    Also, I wrote this for coding practice so it was a good excuse to use it.

    It's O(n) for time complexity, and roughly O(log n) for space complexity.
    Storing 10**9 ids consumes 127 MiB of RAM.
    """

    def __init__(self, id_max: int = 10**6):
        self.id_max = id_max
        self.ids = 1 << self.id_max

    def allocate(self) -> int | None:
        """
        Iterates through a range(0, id_max), doing an
        AND with ids and 1<<id_max. If the result is 0,
        that bit is unallocated, and ids is OR'd with it
        to set the bit.
        """
        for id in range(self.id_max):
            if not self.ids & 1 << id:
                self.ids |= 1 << id
                return id
        return None

    def release(self, id: int):
        self.ids = self.ids - (1 << id)


class Solution:
    """
    Given a terminal output listing directories prefixed with dir,
    and files prefixed with integers, find the sum size of all
    directories having a total size < = 100000. Note that nested
    directories should be counted both individually and with their parent.
    """

    def __init__(self):
        self.alloc_inodes = []
        self.aocd = AOCD(file_path=__file__)
        self.data = [x.split() if x else "" for x in self.aocd.puzzle]
        self.inode = Inode()
        self.render = render
        self.running_total = 0
        self.utilities = Utilities()

    def make_ls_output(
        self, file_name: str, file_size: str, human: bool, inode: int, is_file: bool
    ) -> str:
        def _human_size(file_size: int) -> str:
            for unit in ["B", "K", "M", "G", "T", "P", "E"]:
                if file_size < 1024 or unit == "P":
                    break
                file_size /= 1024
            if unit == "B":
                decimals = 0
            elif file_size < 10:
                decimals = 1
            else:
                decimals = 0
            return f"{file_size:.{decimals}f}{unit}"

        dt = (
            datetime.datetime.now()
            + datetime.timedelta(seconds=random.randrange(-(10**7), 10**7))
        ).strftime("%h %d %H:%M")
        if human:
            file_size = _human_size(int(file_size))
        base_fmt = f"1 sgarland  sgarland {file_size: <4} {dt} {file_name}"

        if is_file:
            return f"{inode: <4} -rw-r--r-- {base_fmt}"
        return f"{inode: <4} drwxr-xr-x {base_fmt}"

    def traverse_fs(self, data):
        """
        Iterates over the input, and for cd, appends '/'-delimited directories
        to a list to build the absolute path. If the directory goes up one level
        with '..', the last item of the list is deleted.

        ls is skipped, because nothing needs to be done except read the next output.

        """

        def _get_inode(self) -> int:
            self.alloc_inodes.append(self.inode.allocate())
            return self.alloc_inodes[-1]

        fs = Node(
            "root",
            inode=_get_inode(self),
            file_size=0,
            ls_line="",
            is_dir=True,
            is_file=False,
        )
        cwd = []
        for line in data:
            if line[0] == "$":
                if line[1] == "cd":
                    if line[2] == "/":
                        cwd.append("root")
                    elif line[2] == "..":
                        del cwd[-1]
                    else:
                        cwd.append(f"{line[2]}")
                continue
            inode = _get_inode(self)
            parent = search.find(
                fs,
                lambda x: "/".join([str(node.name) for node in x.path])
                == "/".join([x for x in cwd]),
            )
            # Directory
            if line[0].isalpha():
                Node(
                    line[1],
                    inode=inode,
                    parent=parent,
                    ls_line=self.make_ls_output(
                        file_name=line[1],
                        file_size=0,
                        human=True,
                        is_file=False,
                        inode=inode,
                    ),
                    file_size=0,
                    is_dir=True,
                    is_file=False,
                )
            # File
            elif line[0].isnumeric():
                Node(
                    line[1],
                    inode=inode,
                    parent=parent,
                    ls_line=self.make_ls_output(
                        file_name=line[1],
                        file_size=line[0],
                        human=True,
                        is_file=True,
                        inode=inode,
                    ),
                    file_size=line[0],
                    is_dir=False,
                    is_file=True,
                )

        return fs

    def solve(self, filesystem: Node):
        file_sizes = sum([int(x.file_size) for x in filesystem.children if x.is_file])
        subdir_sizes = sum(
            [self.solve(x) for x in filesystem.children if not x.is_file]
        )
        total_sizes = file_sizes + subdir_sizes
        if total_sizes <= 100_000:
            self.running_total += total_sizes
        return self.running_total


if __name__ == "__main__":
    s = Solution()
    filesystem = s.traverse_fs(s.data)

    # Print`ls -li` output
    # node_items = [node for node in PostOrderIter(filesystem)]
    # for node in node_items:
    #    print(node.ls_line)

    # Print tree
    # for pre, _, node in s.render.RenderTree(filesystem):
    #    print(f"{pre}{node.name}")
    answer = s.solve(filesystem)
    print(answer)
    # s.aocd.submit_puzzle(answer)
