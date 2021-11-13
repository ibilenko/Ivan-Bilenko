from typing import List
#input
'''6
Insert 200
Insert 10
ExtractMax
Insert 5
Insert 500
ExtractMax'''
#output
'''200
   500'''

n = int(input())
x = 0
l: List[int] = [0]


def siftup(l):
    index = len(l) - 1
    father = int(index / 2)
    while l[father] < l[index] and index > 1:
        change = l[index]
        l[index] = l[father]
        l[father] = change
        index = father
        father = int(index / 2)


def extract_max(l):
    index = len(l) - 1
    maxi = l[1]
    l[1] = l[index]
    l.pop(index)
    return maxi


def son(l, index):
    try:
        son_index = 2 * index
        if l[son_index] < l[2 * index + 1]:
            son_index = 2 * index + 1
        return son_index
    except:
        try:
            son = l[2 * index]
            son_index = 2 * index
            return son_index
        except:
            return 0


def siftdown(l):
    index = 1
    son_index = son(l, index)
    if son_index != 0:
        while l[index] < l[son_index]:
            change = l[index]
            l[index] = l[son_index]
            l[son_index] = change
            index = son_index
            son_index = son(l, index)


while x != n:
    comand: str = input()
    x += 1
    if comand.split(' ')[0] == 'Insert':
        l.append(int(comand.split(' ')[1]))
        siftup(l)
    else:
        print(extract_max(l))
        siftdown(l)
