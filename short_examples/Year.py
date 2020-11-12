def is_leap(y):
    if y % 4 == 0:
        if y % 100 == 0:
            if y % 400 == 0:
                return True
            return False
        return True
    return False


if __name__ == "__main__":
    for yy in [1200, 1900, 1904, 2000]:
        print(yy, is_leap(yy))
