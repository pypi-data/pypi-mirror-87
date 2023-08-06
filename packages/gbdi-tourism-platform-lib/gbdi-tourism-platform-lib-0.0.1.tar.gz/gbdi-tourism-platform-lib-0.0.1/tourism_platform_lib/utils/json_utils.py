from bson import ObjectId
from pymongo.cursor import Cursor
def mongo2json(bson_object):
    if type(bson_object) == Cursor:
        bson_to_list = [{k: v if type(v) != ObjectId else str(v) for k, v in each_object.items()} for each_object in bson_object]
        return bson_to_list
    if type(bson_object) == dict:
        return {k: v if type(v) != ObjectId else str(v) for k, v in bson_object.items()}


