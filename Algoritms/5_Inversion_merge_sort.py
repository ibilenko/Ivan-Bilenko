# input
'''5
2 3 9 2 9'''
#output
'''2'''
def merge(l, r):
    ls = len(l)
    rs = len(r)
    mas = []
    l.sort()
    r.sort()
    inv_new = 0
    if ls == 1 and rs == 1:
        if l[0] > r[0]:
            mas.append(r[0])
            mas.append(l[0])
            inv_new += 1
        else:
            mas.append(l[0])
            mas.append(r[0])
    else:
        i = 0
        j = 0
        while i <= ls - 1 and j <= rs - 1:
            if l[i] > r[j]:
                inv_new += ls - i
                j += 1
            else:
                i += 1
        ri = 0
        li = 0
        while ls != 0 or rs != 0:
            if ls == 0 and rs != 0:
                mas.append(r[ri])
                rs -= 1
                ri += 1
            elif ls != 0 and rs == 0:
                mas.append(l[li])
                ls -= 1
                li += 1
            else:
                if l[0] > r[0]:
                    mas.append(r[ri])
                    rs -= 1
                    ri += 1
                else:
                    mas.append(l[li])
                    ls -= 1
                    li += 1

    return mas, inv_new


def main():
    n = int(input())
    mas = list(map(int, input().split()))
    long = len(mas)
    count = 0
    skoba = 0
    while long != 1:
        new = []
        for i in range(0, long, 2):
            if i + 1 <= long - 1:
                if skoba == 0:
                    res = merge([mas[i]], [mas[i + 1]])
                else:
                    res = merge(mas[i], mas[i + 1])
                new.append(res[0])
                count += res[1]
        if long % 2 != 0 and skoba == 0:
            new.append([mas[long - 1]])
        elif long % 2 != 0 and skoba > 0:
            new.append(mas[long - 1])
        mas = new
        long = len(mas)
        skoba += 1
    print(count)

if __name__ == '__main__':
    main()