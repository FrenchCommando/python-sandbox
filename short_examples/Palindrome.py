import logging
logger = logging.getLogger("")
logger.setLevel(logging.INFO)


def palindrome_key(s):
    return -len(s), s
    # max in length but min in alphabetical order


def biggest_palindrome(s1, s2):
    logging.info("Palindrome Biggest called for: %s - %s", s1, s2)

    def sub_palindrome(i1, i2):
        # biggest palindrome made from subsets of s1 and s2 defined by index
        return palindrome(s1[i1 + 1:] + s2[:i2])
    return min((s1[i1] + sub_palindrome(i1, i2) + s2[i2]
               for i1 in range(len(s1)) for i2 in range(len(s2)) if s1[i1] == s2[i2]),
               key=palindrome_key, default="-1")


def palindrome(s):
    logging.info("Palindrome called for: %s", s)
    # returns the longest palindrome which is a subset of s
    if len(s) <= 1:
        return s
    if s[0] == s[-1]:
        return s[0] + palindrome(s[1:-1]) + s[-1]
    s1, s2 = palindrome(s[1:]), palindrome(s[:-1])
    return min(s1, s2, key=palindrome_key)


def test_palindrome(s1, s2):
    print(s1, "\t", s2, "--->>\t", biggest_palindrome(s1, s2))


if __name__ == "__main__":
    test_palindrome("bac", "bac")  # aba
    test_palindrome("abc", "def")  # ""
    test_palindrome("jdfh", "fds")  # dfhfd
    test_palindrome("AAAAAA", "BBB")  # ""
    test_palindrome("ABCDEF", "FERDCBA")  # "ABCDEFFEDCBA"
