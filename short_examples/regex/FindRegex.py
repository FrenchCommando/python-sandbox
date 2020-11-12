import re


def find_all(s, k):
    m = re.search(k, s)
    if m is None:
        print((-1, -1))
        return
    start_index = 0
    while m is not None:
        print("({}, {})".format(m.start() + start_index,(m.end() + start_index)))
        start_index += m.start() + 1
        m = re.search(k, s[start_index:])


if __name__ == "__main__":
    find_all("aaabbaa", "aa")
    find_all("aaabbaa", "t")
