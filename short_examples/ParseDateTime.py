from datetime import datetime


def parse_date(s):
    return datetime.strptime(s, "%a %d %b %Y %H:%M:%S %z")


if __name__ == "__main__":
    print(parse_date("Sun 10 May 2015 13:54:36 -0700"))
    print(parse_date("Sun 10 May 2015 13:54:36 -0000"))
    print(parse_date("Sat 02 May 2015 19:54:36 +0530"))
    print(parse_date("Fri 01 May 2015 13:54:36 -0000"))
