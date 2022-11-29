class Utilities:

    def get_input() -> list:
        with open("./input.txt", "r") as f:
            ip = f.read().split("\n")
        return ([x for x in ip if x], len(ip[0]))
