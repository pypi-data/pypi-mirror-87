from feature_extractor import FeatureExtractor


def DirectString_V2(feature_desc, depend_list):
    """
    DirectString method
    """
    if len(depend_list) != 1:
        raise ValueError("there must be one depend when use DirectString extract method")
    mod = None
    if feature_desc.arg != -1:
        mod = int(feature_desc.arg[0])
    if depend_list[0] != "":
        hash_value = fe.xxhash(
                depend_list[0] + feature_desc.slot, mod)
    else:
        hash_value = feature_desc.fill_value
    return [hash_value]

fe = FeatureExtractor()
fe.regist_method(DirectString_V2) #change 'DirectString' to 'DirectString-V2' in 'conf/slot_list.conf'
fe.update_proto("rank.proto")
fe.build("./conf/slot_list.conf")
dataset = fe.parse_proto_file("./mergelog.prototxt")
for request in dataset:
    print(fe.extract_from_records(request))
