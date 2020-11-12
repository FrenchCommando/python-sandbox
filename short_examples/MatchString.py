import re
from itertools import combinations


def match_full_string(s1, s2):
    reg = r'.*{}.*'.format(r'.*'.join(s1))
    return re.match(reg, s2)


def match_strings(s1, s2):
    if len(s1) > len(s2):
        return match_strings(s2, s1)
    # ensures len(s1) <= len(s2)
    for i in range(len(s1), -1, -1):
        rep = set()
        for u in combinations(s1, i):
            su = ''.join(u)
            if match_full_string(su, s2):
                rep.add(su)
        if rep:
            return i, rep


def match_strings2(s1, s2):
    if not s1 or not s2:
        return 0, ""
    if s1[0] != s2[0]:
        return max(match_strings2(s1[1:], s2),
                   match_strings2(s1, s2[1:]),
                   key=lambda x: x[0])
    i, s = match_strings2(s1[1:], s2[1:])
    return i + 1, s1[0] + s


def test_matchstrings(s1, s2):
    print(s1, "\t", s2, "--->>\t", match_strings(s1, s2), '\t', match_strings2(s1, s2))


if __name__ == "__main__":
    test_matchstrings("ABAZDC", "BACBAD")
    test_matchstrings("ABCBA", "BAZZCBAD")
    test_matchstrings("AAAAAA", "AAA")
    test_matchstrings("AAAAAA", "BBBBB")
