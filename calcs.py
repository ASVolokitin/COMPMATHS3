from decimal import Decimal

a = 2
b = 4
n = 10
dx = b - a
h = Decimal(dx / n)

def func(x):
    return round(Decimal(-2 * x**3 - 3 * x**2 + x + 5), 5)

def solve_cotes():
    res = 0
    l0 = 41 * func(a)
    l1 = 216 * func(a + h)
    l2 = 27  * func(a + 2 * h)
    l3 = 272  * func(a + 3 * h)
    l4 = 27 * func(a + 4 * h)
    l5 = 216 * func(a + 5 * h)
    l6 = 41 * func(a + 6 * h)
    print(l0, l1, l2, l3, l4, l5, l6)
    res = l0 + l1 + l2 + l3 + l4 + l5 + l6
    res /= 840
    res *= dx
    print(res)

def solve_rectangle():
    res = 0
    x = a + h / 2
    for _ in range(n):
        addon = Decimal(func(x))
        res += addon
        print(round(addon, 5))
        x += h
    return round(Decimal(res) * h, 5)

def solve_trapezoid():
    x = a + h
    res = 0
    print(f"func(a) = {func(a)}, func(b) = {func(b)}")
    for _ in range(n - 1):
        print(f"func(x) = {func(x)}")
        res += func(x)
        x += h
    print(Decimal(func(a) + func(b)) / 2, res)
    res += Decimal(func(a) + func(b)) / 2
    res *= h
    return Decimal(res)

def solve_simpson():
    res = 0
    print(f"func(a) = {func(a)}, func(b) = {func(b)}")
    res += (func(a) + func(b))
    x = a + h
    for i in range(1, n):
        if i % 2 == 0:
            res += 2 * func(x)
        else:
            res += 4 * func(x)
        print(f"i = {i}: func(x) = {func(x)}")
        x += h
    print(res)
    res *= (h / 3)
    return res

print(solve_simpson())