#input
'''4 14
a: 0
b: 10
c: 110
d: 111
01001100100111'''
#output
'''abacabad'''

from typing import Dict, List
d: Dict[str, int] = {}
info = input().split(' ')
for i in range(int(info[0])):
    per = input().split(': ')
    d[per[1]] = per[0]
code = input()
l: List[int] = []
i = 0
while i < len(code):
    n = 0
    row = code[i]
    while n == 0:
        if row in d.keys():
            l.append(d[row])
            n = 1
            i += 1
        else:
            row += code[i+1]
            i += 1
print(''.join(l))