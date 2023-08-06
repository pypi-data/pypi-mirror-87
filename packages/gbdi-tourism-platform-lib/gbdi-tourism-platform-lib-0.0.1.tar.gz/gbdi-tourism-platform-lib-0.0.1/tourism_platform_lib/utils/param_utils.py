from datetime import date, datetime
from time import time
from ast import literal_eval
import re

def check_params(req_args, sample, required = []):
    req_args = dict(req_args)
    assert type(sample) == dict, "Sample must be Dictionary type"
    assert type(required) == list, "Required must be Array type"
    for each_arg in req_args:
        assert each_arg in sample.keys(), "There is no '{}' param in this api".format(each_arg)
    for key, val in sample.items():
        sample_val_type = type(val)
        try:
            if sample_val_type in [int, float, list]:
                req_args[key]  = literal_eval(req_args[key])
                if is_iterable(req_args[key],val):
                    for inner_list_item_1, inner_list_item_2 in zip(req_args[key], val):
                        assert type(inner_list_item_1) == type(inner_list_item_2), "TypeError in sublist on key '{}'".format(key)
                    
            elif sample_val_type in [date]:
                req_args[key] = datetime.strptime(req_args[key], '%Y-%m-%d')
        except KeyError:
            assert key not in required, "Require key '{}' in args ".format(key) 
            continue

    #for each_required_field in required:
    #    assert each_required_field in req_args.keys(), "Missing required field on key '{}'".format(each_required_field)
            
    return req_args
    
def is_iterable(*obj):
    try:
        for item in obj:
            iter_item = iter(item)
        return True
    except TypeError as te:
        return False
    