from operator import add, sub, mul, floordiv, truediv

a = int(input("a"))
b = int(input("b"))
for op in [add, sub, mul, floordiv, truediv]:
    print(op.__name__, op(a, b))
