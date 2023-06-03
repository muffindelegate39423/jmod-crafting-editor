from lib import dictfuncs
import json

craftables = json.loads(open("jmod-crafting-editor/sample/jmod_config.txt",'r').read())["Craftables"]
known_craftingReqs = []
known_categories = []
known_craftingTypes = []

def load_data():
    for c in craftables:
        dictfuncs.add_materials(craftables[c],known_craftingReqs,"craftingReqs")
        dictfuncs.add_to_keyList(craftables[c],known_categories,"category")
        dictfuncs.add_to_keyList(craftables[c],known_craftingTypes,"craftingType")
    known_craftingReqs.sort()
    known_categories.sort()
    known_craftingTypes.sort()

load_data()
print(known_craftingReqs)
print(known_categories)
print(known_craftingTypes)