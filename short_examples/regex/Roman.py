import re

sub_format = "(({0}{2})|{1}?(({0}{1})|{0}{3}))"
regex_pattern = r"^M{0,3}" \
                + "{}{}{}".format(sub_format.format("C", "D", "M", "{0,3}"),
                                  sub_format.format("X", "L", "C", "{0,3}"),
                                  sub_format.format("I", "V", "X", "{0,3}")) \
                + "$"
print(regex_pattern)

letter_mapping = dict(
    M=1000,
    D=500,
    C=100,
    L=50,
    X=10,
    V=5,
    I=1,
)


def check_roman(s):
    return re.match(regex_pattern, s)


def convert_roman(s):
    current = None
    value = 0
    for u in s:
        v = letter_mapping[u]
        if current is None:
            current = v
        else:
            if current < v:
                value -= current
                value += v
                current = None
            else:
                value += current
                current = v
    if current is not None:
        value += current
    return value


def test_roman(s):
    if check_roman(s):
        print(s, convert_roman(s))
    else:
        print(s, "not valid roman string")


if __name__ == "__main__":
    test_roman("MMM")
    test_roman("IM")
    test_roman("XM")
    test_roman("CM")
    test_roman("MMMMMMMMMM")
    test_roman("CCC")
    test_roman("DCD")
    test_roman("CCXXX")
    test_roman("CCCXXI")
    test_roman("CXXIV")
