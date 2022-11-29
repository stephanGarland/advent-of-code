import pathlib

from classes.template import AOCD as Base

class AOCD(Base):
    pass

aocd = AOCD(file_path=__file__)

if __name__ == "__main__":
    print(aocd.text_file)

