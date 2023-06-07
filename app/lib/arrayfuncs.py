def map_indexes(indexList,anotherList):
    index = 0
    while index != len(indexList):
        indexList[index] = anotherList[int(indexList[index])]
        index += 1