#input
'''10 2'''
#output
'''1'''
def fib_mod(n: int, m: int) -> int:
    f0, f1 = 0, 1
    l = [0, 1]
    if m == 0:
        return n
    if n == 0:
        return f0 % m
    elif n == 1:
        return f1 % m
    while True:
        f0, f1 = f1, f1 + f0
        r = f1 % m
        period_pizan = len(l) - 1
        if r == 1 and l[period_pizan] == 0:# условие окончания периода Пизано
            break
        l.append(r)
    number = n % period_pizan
    return l[number]


def main():
    n, m = map(int, input().split())
    print(fib_mod(n, m))


if __name__ == "__main__":
    main()
