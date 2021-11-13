import sys
from collections import Counter
#input
'''
abacabad
'''
#output
'''
4 14
a: 0
b: 10
c: 110
d: 111
01001100100111
'''
x = sys.stdin.readline()
l = Counter(x).most_common()
len_l = len(l)
l.pop(len(l) - 1)
numbers = []
d = {}

def getKey(item):
    return item[1]
def binaryUnit(l):
    if len(l) != 1:
        l.sort(key=getKey, reverse=True)
        end = len(l)
        left = l[end - 2][0], l[end - 2][1], 0
        numbers.append(left)
        right = l[end - 1][0], l[end - 2][1], 1
        numbers.append(right)
        new = l[end - 2][0] + l[end - 1][0], l[end - 2][1] + l[end - 1][1]
        l.pop(end - 1)
        l.pop(end - 2)
        l.append(new)
        if len(l) == 1:
            numbers.sort(key=getKey, reverse=True)
            return l, numbers
        else:
            binaryUnit(l)
    else:
        return l, numbers

if len(l) == 1:
    trigger = True
else:
    binaryUnit(l)
    trigger = False
for row in l[0][0]:
    for i in range(len(numbers)):
        if row in numbers[i][0]:
            try:
                d[row] = d[row] + str(numbers[i][2])
            except:
                d[row] = str(numbers[i][2])
if trigger:
    d[l[0][0]] = '0'
final = []
for row in x:
    if row != '\n':
        final.append(d[row])

print((len_l - 1), len(''.join(final)))

for row in d.keys():
    print(f'{row}: {d[row]}')
print(''.join(final))



