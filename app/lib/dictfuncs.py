# returns supported jmod versions
def _get_supported_versions():
    supported_versions = ('40.0','40.6','42.5','43.0')
    return supported_versions

# is the config valid (readable)?
def is_valid_config(config_txt):
    craftables_test = config_txt.get('Craftables',-1)
    version_test = get_jmod_version(config_txt)
    if craftables_test != -1 and version_test != -1:
        return True
    else:
        return False

# returns jmod version from config file
def get_jmod_version(config_txt):
    version = config_txt.get('Version',-1)
    if version == -1: # since around version 42.5
        version = config_txt['Info'].get('Version',-1)
    return version

# is the config file supported?
def is_supported_version(jmod_version):
    if str(jmod_version) in _get_supported_versions():
        return True
    else:
        return False

# overrides current craftable data to jmod dict
def set_craftable_data(jmod_dict,jmod_version,oldName,newName,size_scale,crafting_reqs,results,category,crafting_type,description):
    # parse data in order
    data = {}
    data['craftingReqs'] = crafting_reqs
    data['results'] = results
    if size_scale != -1: # if size scale was enabled
        data['sizescale'] = size_scale # set it
    data['category'] = category
    data['craftingType'] = crafting_type
    data['description'] = description
    # try to replace old craftable data
    try:
        jmod_dict['Craftables'][oldName] = data
        if oldName != newName: # rename craftable
            jmod_dict['Craftables'][newName] = jmod_dict['Craftables'].pop(oldName)
    except KeyError: # if it's a new craftable then add it to dictionary
        jmod_dict['Craftables'][newName] = data

# retrieves current craftable data from jmod dict
def get_craftable_data(jmod_dict,jmod_version,craftable_name,size_scale,crafting_reqs,results,category,crafting_type,description):
    data = jmod_dict['Craftables'][craftable_name]
    # keys for each data in the for loop
    keys = {id(size_scale): "sizescale", 
            id(crafting_reqs): "craftingReqs", 
            id(results): "results", 
            id(category): "category", 
            id(crafting_type): "craftingType", 
            id(description): "description"}
    # return each data to variables
    for i in (size_scale,crafting_reqs,results,category,crafting_type,description):
        try:
            i.append(data[keys[id(i)]])
        except KeyError:
            pass

# returns craftable name from jmod dict
def get_craftable_names(jmod_dict,jmod_version):
    temp = []
    for c in jmod_dict['Craftables']:
        temp.append(c)
    return temp

# removes selected craftables from jmod dict
def remove_craftables(jmod_dict,jmod_version,selected_craftables):
    for s in selected_craftables:
        del jmod_dict['Craftables'][s]

# returns categories from jmod dict
def get_categories(jmod_dict,jmod_version):
    temp = []
    for c in jmod_dict['Craftables']:
        try:
            curCategory = jmod_dict['Craftables'][c]['category']
            if curCategory not in temp:
                temp.append(curCategory)
        except KeyError:
            pass
    temp.sort()
    return temp

# returns crafting types from jmod dict
def get_crafting_types(jmod_dict,jmod_version):
    temp = []
    for c in jmod_dict['Craftables']:
        try:
            curType = jmod_dict['Craftables'][c]['craftingType']
            if curType not in temp:
                temp.append(curType)
        except KeyError:
            pass
    temp.sort()
    return temp

# returns crafting reqs from jmod dict
def get_crafting_reqs(jmod_dict,jmod_version):
    temp = []
    for c in jmod_dict['Craftables']:
        for r in jmod_dict['Craftables'][c]['craftingReqs']:
            try:
                if r not in temp:
                    temp.append(r)
            except KeyError:
                pass
    temp.sort()
    return temp

# creates new craftable in jmod dict
def create_new_craftable(jmod_dict,jmod_version,craftable_name):
    # assembles data in order
    data = {}
    data['craftingReqs'] = {}
    data['results'] = ""
    data['category'] = ""
    data['craftingType'] = ""
    data['description'] = ""
    # add to dict
    jmod_dict['Craftables'][craftable_name] = data

# sorts craftables in jmod dict in alphabetical order
def sort_craftables(jmod_dict,jmod_version):
    jmod_dict['Craftables'] = dict(sorted(jmod_dict['Craftables'].items()))