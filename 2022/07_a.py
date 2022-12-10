import collections

from classes.template import AOCD as Base


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
        self.data = [int(x) if x else "" for x in self.aocd.puzzle]
        self.utilities = Utilities()

    # https://gist.github.com/hrldcpr/2012250
    def tree():
        return collections.defaultdict(tree)

    def traverse_dir(self):
        fs = tree()
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

"""
In [87]:  for k, v in fs.items():
print(f"{k}:\n\t{[[[file for file in v.keys()], ''.join([size for size in x.keys()])] for x in v.values()]}")
/:
	[[['a', 'b.txt', 'c.dat', 'd'], ''], [['a', 'b.txt', 'c.dat', 'd'], '14848514'], [['a', 'b.txt', 'c.dat', 'd'], '8504156'], [['a', 'b.txt', 'c.dat', 'd'], '']]
/a/:
	[[['e', 'f', 'g', 'h.lst'], ''], [['e', 'f', 'g', 'h.lst'], '29116'], [['e', 'f', 'g', 'h.lst'], '2557'], [['e', 'f', 'g', 'h.lst'], '62596']]
/a/e/:
	[[['i'], '584']]
/d/:
	[[['j', 'd.log', 'd.ext', 'k'], '4060174'], [['j', 'd.log', 'd.ext', 'k'], '8033020'], [['j', 'd.log', 'd.ext', 'k'], '5626152'], [['j', 'd.log', 'd.ext', 'k'], '7214296']]
"""



if __name__ == "__main__":
    s = Solution()
