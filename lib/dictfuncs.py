import json

def add_to_materials(craftable, materialsList, materialsKey):
    try:
        for val in craftable[materialsKey]:
            if val not in materialsList:
                materialsList.append(val)
    except KeyError:
        pass

def add_to_keyList(craftable, keyList, key):
    try:
        val = craftable[key]
        if val not in keyList:
            keyList.append(val)
    except KeyError:
        pass

def is_valid_config(jmod_config_txt):
    try:
        temp = json.loads(open(jmod_config_txt,'r').read())["Craftables"]
        return True
    except:
        return False