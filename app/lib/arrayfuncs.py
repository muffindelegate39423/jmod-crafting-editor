def map_indexes(indexList,anotherList):
    index = 0
    while index != len(indexList):
        indexList[index] = anotherList[int(indexList[index])]
        index += 1

def get_matching_items(searchStr,itemList):
    matching_items = []
    searchStr = searchStr.lower()
    for i in itemList:
        temp = i.lower()
        if temp.find(searchStr) != -1:
            matching_items.append(i)
    return matching_items