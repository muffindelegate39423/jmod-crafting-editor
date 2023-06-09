import json

def __insert_from_2D_dict(craftable,keyList,key):
    try:
        for val in craftable[key]:
            if val not in keyList:
                keyList.append(val)
    except KeyError:
        pass

def __insert_from_1D_dict(craftable,keyList,key):
    try:
        val = craftable[key]
        if val not in keyList:
            keyList.append(val)
    except KeyError:
        pass

def is_valid_config(config_txt):
    try:
        temp = get_craftables(config_txt)
        return True
    except:
        return False

def get_craftables(config_txt):
    return json.loads(open(config_txt,'r').read())["Craftables"]

def get_craftable_properties(craftables,craftableNames,knownCraftingReqs,knownCategories,knownCraftingTypes):
    for c in craftables:
        craftableNames.append(c)
        __insert_from_2D_dict(craftables[c],knownCraftingReqs,"craftingReqs")
        __insert_from_1D_dict(craftables[c],knownCategories,"category")
        __insert_from_1D_dict(craftables[c],knownCraftingTypes,"craftingType")

def get_craftable_data(craftablesDict,craftableName,sizeScale,craftingReqs,results,category,craftingType,description):
    data = craftablesDict[craftableName]
    keys = {id(sizeScale): "sizescale", 
            id(craftingReqs): "craftingReqs", 
            id(results): "results", 
            id(category): "category", 
            id(craftingType): "craftingType", 
            id(description): "description"}
    for i in (sizeScale,craftingReqs,results,category,craftingType,description):
        try:
            i.append(data[keys[id(i)]])
        except KeyError:
            pass

def remove_craftables(craftablesDict,selectedCraftables):
    for s in selectedCraftables:
        del craftablesDict[s]