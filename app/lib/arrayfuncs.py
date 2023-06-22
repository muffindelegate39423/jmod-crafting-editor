from . import strmanip

# function that returns matching items from list
# based on substring
def get_matching_items(substring,itemList):
    matching_items = []
    substring = strmanip.format_search_string(substring)
    for i in itemList:
        temp = strmanip.format_search_string(i)
        if temp.find(substring) != -1:
            matching_items.append(i)
    return matching_items

# function that maps indexes with values from another list
def map_indexes(indexList,anotherList):
    index = 0
    while index != len(indexList):
        indexList[index] = anotherList[int(indexList[index])]
        index += 1