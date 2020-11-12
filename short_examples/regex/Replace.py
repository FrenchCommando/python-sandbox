import re


def replace_str(f, t, s):
    return s.replace(f, t)


def replace_str_reg(f, t, s):
    def rr(u):
        return t
    return re.sub(f, rr, s)


if __name__ == "__main__":
    print(replace_str(" && ", " and ", "if me && you"))
    print(replace_str_reg(" && ", " and ", "if me && you"))
    print(replace_str_reg(" \|\| ", " or ", "if me || you"))
