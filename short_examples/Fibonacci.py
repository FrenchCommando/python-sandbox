import time  # to compare execution time - otherwise there is not import
import matplotlib.pyplot as plt


def fib(n):
    def f():
        a, b = 1, 1
        yield a
        yield b
        while True:
            a, b = b, a + b
            yield b
    it = f()
    for v in range(n):
        next(it)
    return next(it)


def log_fib(n):
    def multiply(a, b):
        a00, a01, a10, a11 = a
        b00, b01, b10, b11 = b
        return a00 * b00 + a01 * b10,\
            a00 * b01 + a01 * b11,\
            a10 * b00 + a11 * b10,\
            a10 * b01 + a11 * b11

    def multiply_v(a, x):
        a00, a01, a10, a11 = a
        x0, x1 = x
        return a00 * x0 + a01 * x1,\
            a10 * x0 + a11 * x1

    class MMatrix:
        def __init__(self):
            self.d = {
                0: (1, 0, 0, 1),  # this is not really necessary
                1: (0, 1, 1, 1)
            }

        def get(self, i):
            if i in self.d:
                return self.d[i]
            if i % 2 == 0:
                mm = self.get(i // 2)
                t = multiply(mm, mm)
                self.d[i] = t
                return t
            if i % 2 == 1:
                mm = self.get(i - 1)
                t = multiply(mm, self.d[1])
                self.d[i] = t
                return t

    m = MMatrix()
    x = (0, 1)
    r0, r1 = multiply_v(m.get(n), x)
    return r1


def test_matching_fib(n):
    print("n = {}".format(n), end=" -- ")
    print("value {}".format(fib(n)), end=" - ")
    print("valueLog {}".format(log_fib(n)), end=" - ")

    number_exec = 10000
    start = time.time()
    for w in range(number_exec):
        fib(n)
    mid = time.time()
    for w in range(number_exec):
        log_fib(n)
    end = time.time()
    ftime = round(1000 * (mid - start))
    ltime = round(1000 * (end - mid))
    print("Timing :regular {} - log {}".format(ftime, ltime), end="")
    print()
    return ftime, ltime


if __name__ == "__main__":
    global_n = 200
    t = {}
    for u in range(global_n):
        f, l = test_matching_fib(u)
        t[u] = f, l
    plt.plot([u for u in t], [v[0] for v in t.values()], label="Fib")
    plt.plot([u for u in t], [v[1] for v in t.values()], label="Log")
    plt.legend()
    plt.show()
