"""
feature extractor
"""
#encoding=utf-8
import os
import six
import sys
import time
import collections
import importlib
import ujson
from collections import Iterable
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from lib.method_list import DirectString, TopString, LastString, Int, WordSegment, FExxhash, Normalization
from feature_config import FeatureDesc, FeatureConfig
from utils import compile_proto, json2proto


class FeatureExtractor():
    """
    FeatureExtractor Class
    """
    def __init__(self):
        self._feature_id = 0
        self.feature_id_map = {}
        self.feature_value_map = {}
        self.origin_feature_name_list = []
        self.origin_feature_num = 0
        self.feed_feature_list = []
        self.feed_feature_name_list = []
        self.method = {}
        self.xxhash = FExxhash
        self.proto = "ex_proto.rank_pb2"

    def build(self, conf_file, proto_file=None):
        """
        load config and method
        """
        self.parse_conf(conf_file)
        self.feed_feature_num = len(self.feed_feature_list)
        self.feed_feature_value_list = [[] for i in range(self.feed_feature_num)]

        self.regist_method(DirectString)
        self.regist_method(TopString)
        self.regist_method(LastString)
        self.regist_method(Int)
        self.regist_method(WordSegment)
        self.regist_method(Normalization)

        self.update_proto(proto_file)

    def update_proto(self, proto_file_path):
        """
        update proto
        """
        if proto_file_path is None:
            return
        proto_file_path = os.path.abspath(proto_file_path)
        proto_file_path, proto_file_name = os.path.split(proto_file_path)
        cur_path = os.getcwd()
        os.chdir(proto_file_path)
        compile_proto(proto_file_name)
        proto_pyfile_name = proto_file_name.split(".")[0] + "_pb2.py"
        module_path = os.path.abspath(os.path.dirname(__file__))
        ret = os.system("cp {} {}".format(proto_pyfile_name,
            os.path.join(module_path, "ex_proto")))
        if ret != 0:
            print("update proto failed")
        os.chdir(cur_path)
        sys.path.append(module_path)
        self.proto = "ex_proto.{}".format(proto_pyfile_name.split(".")[0])
        self.pb2 = importlib.import_module(self.proto)

    def parse_conf(self, conf_file):
        """
        parse config file
        """
        if not os.path.isfile(conf_file):
            raise IOError("No this slot conf file: {} not exist".format(conf_file))
        with open(conf_file) as f:
            for line in f.readlines():
                if len(line) == 0 or line[0] == '#':
                    continue
                if "origin_feature" in line:
                    self._add_origin_feature(line)
                elif "feature_name" in line:
                    self._add_feature(line)

    def parse_proto_file(self, file_name):
        """
        parse prototxt to protobuf
        """
        dataset = self.pb2.Dataset()
        with open(file_name, "rb") as f:
            dataset.ParseFromString(f.read())
        return dataset.msg

    def _add_feature(self, line):
        """
        add target feature
        """
        feature_config = FeatureConfig(line)
        feature_desc = FeatureDesc(feature_config, self.feature_id_map, self._feature_id)
        self.feed_feature_list.append(feature_desc)
        self.feature_id_map[feature_desc.name] = self._feature_id
        self.feed_feature_name_list.append(feature_desc.name)
        self._feature_id += 1

    def _add_origin_feature(self, line):
        """
        add origin feature
        """
        self.origin_feature_name_list = line.split(":")[1].strip().split(",")
        self.origin_feature_num = len(self.origin_feature_name_list)
        for origin_feature_name in self.origin_feature_name_list:
            self.feature_id_map[origin_feature_name] = self._feature_id
            self._feature_id += 1

    def regist_method(self, method):
        """
        regist method
        """
        if method.__name__ in self.method:
            print("This method name is already registed.")
            return -1
        self.method[method.__name__] = method
        return 0

    def _get_origin_feature_value_by_name(self, name, ins, idx):
        """
        get origin feature value by name
        """
        name_list = name.split(".")
        target = ins

        for name in name_list:
            if name == "item_info":
                if isinstance(target, dict):
                    target = target[name][idx]
                else:
                    target = getattr(target, name)[idx]
            elif "*" in name:
                name = name.split("[")[0]
                if isinstance(target, dict):
                    target = target[name]
                else:
                    target = getattr(target, name)[:]
            else:
                if isinstance(target, list):
                    target = [ getattr(target_elem, name) for target_elem in target ]
                elif isinstance(target, dict):
                    target = target[name]
                else:
                    target = getattr(target, name)
        if isinstance(target, Iterable) and not isinstance(target, (str, six.text_type)):
            return target
        else:
            return [target]

    def _get_all_origin_feature_value(self, ins, idx):
        """
        get all origin feature value from protobuf
        """
        for origin_feature_name in self.origin_feature_name_list:
            self.feature_value_map[origin_feature_name] = self._get_origin_feature_value_by_name(
                    origin_feature_name, ins, idx)

    def extract_from_json(self, batch_ins):
        """
        extract feature from json
        """

        self.feed_feature_value_list = [[] for i in range(self.feed_feature_num)]
        if isinstance(batch_ins, str):
            batch_data = [batch_ins]
        elif isinstance(batch_ins, list):
            batch_data = batch_ins
        else:
            raise ValueError("extract_from_json not support type {}".format(type(batch_ins)))
        for ins in batch_data:
            ins = ujson.loads(ins)
            if "item_info" not in ins:
                raise ValueError("The json instance must contain the 'item_info' field.")
            if not isinstance(ins["item_info"], Iterable):
                raise ValueError("The item_info must be Iterable.")
            for idx in range(len(ins["item_info"])):
                instance_feature_value_list = self._extract_instance(ins, idx)
                for idx, feature in  enumerate(self.feed_feature_list):
                    self.feed_feature_value_list[idx].append(
                            instance_feature_value_list[idx])

        result_dict = collections.OrderedDict()
        for idx, slot in enumerate(self.feed_feature_name_list):
            result_dict[slot] = self.feed_feature_value_list[idx]
        return result_dict

    def extract_from_records(self, batch_ins):
        """
        extract feature from protobuf
        """
        self.feed_feature_value_list = [[] for i in range(self.feed_feature_num)]
        if isinstance(batch_ins, self.pb2.Dataset):
            batch_data = batch_ins.msg
        elif isinstance(batch_ins, list):
            batch_data = batch_ins
        elif isinstance(batch_ins, self.pb2.Msg_Class):
            batch_data = [batch_ins]
        else:
            raise ValueError("extract_from_records not support type {}".format(type(batch_ins)))
        for ins in batch_data:
            if not hasattr(ins, "item_info"):
                raise ValueError("The protobuf instance must contain the 'item_info' field.")
            if not isinstance(ins.item_info, Iterable):
                raise ValueError("The item_info must be Iterable.")
            for item_idx in range(len(ins.item_info)):
                instance_feature_value_list = self._extract_instance(ins, item_idx)
                for idx, feature in  enumerate(self.feed_feature_list):
                    self.feed_feature_value_list[idx].append(
                            instance_feature_value_list[idx])

        result_dict = collections.OrderedDict()
        for idx, slot in enumerate(self.feed_feature_name_list):
            result_dict[slot] = self.feed_feature_value_list[idx]
        return result_dict

    def extract_from_records_for_predict(self, batch_ins):
        """
        extract feature from protobuf for predict
        """
        for feature in self.feed_feature_list:
            if feature.predict == "0":
                self.feed_feature_list.remove(feature)
                self.feed_feature_name_list.remove(feature.name)
        return self.extract_from_records(batch_ins)

    def extract_from_records_pair(self, user_info=None, item_info=None):
        """
        extract feature from multi protobuf
        """
        self.feed_feature_value_list = [[] for i in range(self.feed_feature_num)]
        if not isinstance(user_info, self.pb2.Msg_Class.user_info_Class):
            raise ValueError("Plese make sure user_info is Msg_Class.user_info_Class")
        if not isinstance(item_info, Iterable):
            if isinstance(item_info, self.pb2.Msg_Class.item_info_Class):
                item_info = [item_info]
            else:
                raise ValueError("Plese make sure item_info is Msg_Class.user_info_Class or RepeatedCompositeContainer")
        records_map = {"user_info":user_info, "item_info":item_info}
        for item_idx in range(len(records_map["item_info"])):
            instance_feature_value_list = self._extract_instance(records_map, item_idx)
            for idx, feature in  enumerate(self.feed_feature_list):
                self.feed_feature_value_list[idx].append(
                    instance_feature_value_list[idx])
        result_dict = collections.OrderedDict()
        for idx, slot in enumerate(self.feed_feature_name_list):
            result_dict[slot] = self.feed_feature_value_list[idx]
        return result_dict

    def extract_from_records_pair_for_predict(self, user_info=None, item_info=None):
        """
        extract feature from multi protobuf for predict
        """
        for feature in self.feed_feature_list:
            if feature.predict == "0":
                self.feed_feature_list.remove(feature)
                self.feed_feature_name_list.remove(feature.name)
        return self.extract_from_records_pair(user_info, item_info)

    def _extract_instance(self, ins, idx):
        """
        extract instance
        """
        instance_feature_value_list = [[] for i in range(self.feed_feature_num)]
        #clear map
        self.feature_value_map = {}

        for key in self.feed_feature_name_list:
            self.feature_value_map[key] = []
        self._get_all_origin_feature_value(ins, idx)
        for idx, feature_desc in  enumerate(self.feed_feature_list):
            depend_dict = {depend:self.feature_value_map[depend]
                    for depend in feature_desc.depend }
            self.feature_value_map[feature_desc.name] = self.method[feature_desc.method](
                    feature_desc, depend_dict)
            instance_feature_value_list[idx]= self.feature_value_map[feature_desc.name]
        return instance_feature_value_list

if __name__ == "__main__":
    #from proto
    fe = FeatureExtractor()
    fe.build("./conf/slot_list.conf", "rank.proto")
    file_name = "./mergelog.prototxt"
    dataset = fe.parse_proto_file(file_name)
    for request in dataset:
        feed_data = fe.extract_from_records(request)
        #print(feed_data)

    #from json
    fe = FeatureExtractor()
    fe.build("./conf/slot_list.conf")
    with open("./mergelog-100.json") as f:
        for line in f.readlines():
            feed_data = fe.extract_from_json(line)
            print(feed_data)
