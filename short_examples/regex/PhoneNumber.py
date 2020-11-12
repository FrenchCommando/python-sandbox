import re


def is_phone(n):
    return re.match(r"^[789][0-9]{9}$", n)


def test_isphone(n):
    print(n, bool(is_phone(n)))


if __name__ == "__main__":
    test_isphone("9324857444")
    test_isphone("2324857444")
    test_isphone("232485744664")
    test_isphone("932485744664")
