import json

def insert_from_2D_dict(craftable, keyList, key):
    try:
        for val in craftable[key]:
            if val not in keyList:
                keyList.append(val)
    except KeyError:
        pass

def insert_from_1D_dict(craftable, keyList, key):
    try:
        val = craftable[key]
        if val not in keyList:
            keyList.append(val)
    except KeyError:
        pass

def is_valid_config(config_txt):
    try:
        temp = json.loads(open(config_txt,'r').read())["Craftables"]
        return True
    except:
        return False