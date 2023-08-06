import json
from bson import json_util

from bson import ObjectId

def prep_mongo(obj):
    temp_dict = {}
    for k in obj.keys():
        #cast ObjId type to str
        if type(obj[k]) == ObjectId:
            temp_dict[k] = str(obj[k])
        #cast empty dict and list ({}, []) to None
        elif obj[k] not in [{},[]]:
            temp_dict[k] = obj[k]

    return temp_dict

def render_as_json(mongo_output):
    try:
        #if mongo_output is iterable
        result = [prep_mongo(item.to_mongo().to_dict()) for item in mongo_output]
    except AttributeError:
        #else
        result = prep_mongo(mongo_output.to_mongo().to_dict())

    return result