import os

class FeatureConfig(object):
    """
    Feature Config
    """
    def __init__(self, line):
        """
        constructor
        """
        attrs = line.strip().split(';')
        self.arg = -1
        self.padding_len = 1
        self.fill_type = None
        self.fill_value = None

        for attr in attrs:
            kv = attr.strip().split('=')
            if kv[0] == "feature_name":
                self.name = kv[1]
            elif kv[0] == "method":
                self.method = kv[1]
            elif kv[0] == "slot":
                self.slot = kv[1]
            elif kv[0] == "depend":
                self.depend = kv[1].strip().split(',')
            elif kv[0] == "arg":
                self.arg = kv[1].strip().split(",")
            elif kv[0] == "padding_len":
                self.padding_len = int(kv[1])
            elif kv[0] == "fill":
                self.fill_type,self.fill_value= kv[1].strip().split(",")
        fill_func = {"int":int,
                "int64":long,
                "string":str,
                "float":float,
                "bool":bool}
        if self.fill_type != None and self.fill_value != None:
            if self.fill_type not in fill_func:
                raise ValueError("Not support fill {} with {} type.".format(
                    self.name, self.fill_type))
            else:
                self.fill_value = fill_func[self.fill_type](self.fill_value)

class FeatureDesc(object):
    """
    Feature
    """
    def __init__(self, config, feature_id_map, featrue_id):
        """
        constructor
        """
        self.name = config.name
        self.method = config.method
        self.slot = config.slot
        self.feature_id = featrue_id
        self.arg = config.arg
        self.padding_len = config.padding_len
        self.depend = []
        self.fill_type = config.fill_type
        self.fill_value = config.fill_value
        for dp in config.depend:
            if not dp in feature_id_map.keys():
                raise ValueError("depend: {} is not exist".format(dp))             
            self.depend.append(dp)
