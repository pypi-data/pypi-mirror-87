"""
method list
"""
import xxhash
import numpy as np

def FExxhash(target, mod=None):
    """
    hash func
    """
    hash_value = xxhash.xxh64_intdigest(target.encode('utf-8'))
    hash_value = np.array(hash_value).astype("int64").tolist()
    if mod is not None:
        return hash_value % mod
    else:
        return hash_value

def DirectString(feature_desc, depend_dict):
    """
    DirectString method
    """
    if len(depend_dict) != 1:
        raise ValueError("there must be one depend when use DirectString extract method")
    mod = None
    if feature_desc.arg != -1:
        mod = int(feature_desc.arg[0])
    if depend_dict[feature_desc.depend[0]] != "":
        hash_value = [FExxhash(
                value + feature_desc.slot, mod)
                for value in depend_dict[feature_desc.depend[0]]]
    else:
        hash_value = [feature_desc.fill_value]
    return hash_value

def TopString(feature_desc, depend_dict):
    """
    TopString method
    """
    if len(depend_dict) != 1:
        raise ValueError("there must be one depend when use TopString extract method")
    mod = None
    top = None
    if feature_desc.arg != -1:
        top = int(feature_desc.arg[0])
        if len(feature_desc.arg) == 2:
            mod = int(feature_desc.arg[1])
    len_features = len(depend_dict[feature_desc.depend[0]])
    if top > 0 and len_features > top:
        len_features = top
    if len_features > 0:
        hash_value = [ FExxhash(
            depend_dict[feature_desc.depend[0]][idx] + feature_desc.slot, mod)
                for idx in range(len_features)]
    else:
        hash_value = [feature_desc.fill_value]

    return hash_value

def LastString(feature_desc, depend_dict):
    """
    LastString method
    """
    if len(depend_dict) != 1:
        raise ValueError("there must be one depend when use TopString extract method")
    mod = None
    top = None
    if feature_desc.arg != -1:
        top = int(feature_desc.arg[0])
        if len(feature_desc.arg) == 2:
            mod = int(feature_desc.arg[1])
    len_features = len(depend_dict[feature_desc.depend[0]])
    start = 0
    end = len_features
    if top > 0 and len_features > top:
        start = len_features - top
    if len_features > 0:
        hash_value = [ FExxhash(
            depend_dict[feature_desc.depend[0]][idx] + feature_desc.slot, mod)
                for idx in range(start, end)]
    else:
        hash_value = [feature_desc.fill_value]
    return hash_value

def Int(feature_desc, depend_dict):
    """
    string to int
    """
    if len(depend_dict) != 1:
        raise ValueError("there must be one depend when use Int extract method")
    return [int(i) for i in depend_dict[feature_desc.depend[0]]]

def WordSegment(feature_desc, depend_dict):
    """
    word segment
    """
    if len(depend_dict) != 1:
        raise ValueError("there must be one depend when use TopString extract method")
    if len(feature_desc.depend) != 1:
        raise ValueError("feature_desc.depend's length must be 1")
    res = []
    for x in depend_dict[feature_desc.depend[0]]:
        res.append(x)
    return res

def Normalization(feature_desc, depend_dict):
    """
    normalization
    """
    if len(depend_dict) != 1:
        raise ValueError("there must be one depend when use  extract method")
    min_num = float(feature_desc.arg[0])
    max_num = float(feature_desc.arg[1])
    res = [(float(num) - min_num)/(max_num - min_num) for num in depend_dict[feature_desc.depend[0]]]
    return res

