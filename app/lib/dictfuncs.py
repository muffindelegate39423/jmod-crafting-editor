from ast import literal_eval

_STATIC_CRAFTING_TYPE_VERSIONS = ['40.0','40.6','42.5','43.0'] # versions that only allow one crafting type per item
_DYNAMIC_CRAFTING_TYPE_VERSIONS = ['49.6'] # versions that allow for multiple crafting types for items

# returns supported jmod versions
def _get_supported_versions():
    supported_versions = _STATIC_CRAFTING_TYPE_VERSIONS + _DYNAMIC_CRAFTING_TYPE_VERSIONS
    return supported_versions

# does the jmod version support multiple crafting types per item?
def supports_dynamic_crafting_types(jmod_version):
    try:
        jmod_version = float(jmod_version)
        return (jmod_version in _DYNAMIC_CRAFTING_TYPE_VERSIONS) or (jmod_version >= float(_DYNAMIC_CRAFTING_TYPE_VERSIONS[0]))
    except ValueError:
        return False

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

# for loading: formats crafting types of each item for jmod dict (for version 49.6 and later)
def format_crafting_types(jmod_dict):
    for c in jmod_dict['Craftables']:
        curType = jmod_dict['Craftables'][c]['craftingType']
        isList = type(curType) == list
        if isList:
            delim = " "
            curType = delim.join([d for d in curType])
            jmod_dict['Craftables'][c]['craftingType'] = curType
    return jmod_dict

# for saving: fixes crafting types for each item in jmod dict (for version 49.6 and later)
def fix_crafting_types(jmod_dict):
    for c in jmod_dict['Craftables']:
        curType = jmod_dict['Craftables'][c]['craftingType']
        delim = " "
        hasSpace = curType.find(delim) != -1
        if hasSpace:
            curType = curType.split(delim)
            jmod_dict['Craftables'][c]['craftingType'] = curType
    return jmod_dict

# for loading: formats results of each item for jmod dict
def format_results(jmod_dict):
    for c in jmod_dict['Craftables']:
        curResults = jmod_dict['Craftables'][c]['results']
        jmod_dict['Craftables'][c]['results'] = str(curResults)
    return jmod_dict

# for saving: fixes results of each item in jmod dict
def fix_results(jmod_dict):
    for c in jmod_dict['Craftables']:
        curResults = jmod_dict['Craftables'][c]['results']
        isString = type(curResults) == str
        if isString:
            try:
                temp = literal_eval(curResults)
                isList = type(temp) == list
                if isList:
                    jmod_dict['Craftables'][c]['results'] = temp
            except:
                pass
    return jmod_dict

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
    temp = set()
    for c in jmod_dict['Craftables']:
        try:
            curType = jmod_dict['Craftables'][c]['craftingType']
            isList = type(curType) == list
            # fix for 49.6
            if isList:
                for d in curType:
                    temp.add(d)
            else:
                temp.add(curType)
        except KeyError:
            pass
    temp = list(temp)
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