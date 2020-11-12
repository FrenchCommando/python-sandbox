import re
from email.utils import parseaddr


username_pattern = r"[a-zA-Z0-9][a-zA-Z0-9\-_.]+"
domain_pattern = r"[a-zA-Z]*"
extension_pattern = r"[a-zA-Z]{1,3}"
regex_pattern = r"^{}@{}\.{}$".format(username_pattern, domain_pattern, extension_pattern)
print(regex_pattern)


def is_validemail(n):
    name, email = parseaddr(n)
    return re.match(regex_pattern, email)


def test_isvalidemail(n):
    print(n, bool(is_validemail(n)))


if __name__ == "__main__":
    test_isvalidemail("DOSHI <DOSHI@hackerrank.com>")
    test_isvalidemail("DOSHI <DOSHI@hackerrank.c>")
    test_isvalidemail("DOSHI <DOSHI@u.com>")
    test_isvalidemail("DOSHI <DOSHI@.com>")
    test_isvalidemail("DOSHI <DOSHI@hackerrank.coiugigom>")
    test_isvalidemail("DOSHI <DOSHI@hackerrankcoiugigom>")
    test_isvalidemail("DOSHI <-DOSHI@hackerrank.com>")
    test_isvalidemail("DOSHI <DO--HI@hackerrank.com>")
    test_isvalidemail("DOSHI <DO-.HI@hackerrank.com>")
    test_isvalidemail("DOSHI <DO_HI@hackerrank.com>")