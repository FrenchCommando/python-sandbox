class Memoize:
    def __init__(self, func):
        self.func = func
        self.data = {}

    def __call__(self, *args):
        if args in self.data:
            return self.data[args]
        rep = self.func(*args)
        self.data[args] = rep
        return rep


@Memoize
def solve_prefix(s1, s2):
    if not s1 or not s2:
        return ""
    if s1[0] != s2[0]:
        return ""
    return s1[0] + solve_prefix(s1[1:], s2[1:])


m_solve = Memoize(solve_prefix)


@Memoize
def match_substrings(s1, s2):
    return max((solve_prefix(s1[i:], s2[j:]) for i in range(len(s1)) for j in range(len(s2))), key=len)


def test_matchsubstrings(s1, s2):
    print(s1, "\t", s2, "--->>\t", match_substrings(s1, s2))


if __name__ == "__main__":
    test_matchsubstrings("ABAZDC", "BACBAD")
    test_matchsubstrings("ABCBA", "BAZZCBAD")
    test_matchsubstrings("AAAAAA", "AAA")
    test_matchsubstrings("AAAAAA", "BBBBB")
