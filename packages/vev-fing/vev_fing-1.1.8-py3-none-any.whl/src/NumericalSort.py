import re
numbers = re.compile(r'(\d+)')
def numericalSort(value): #numerical sort used in readData
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts