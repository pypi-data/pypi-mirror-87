#encoding=utf-8
import os
import sys
import xxhash
import ujson
import time
import unittest

class FETest(unittest.TestCase):

    #check result 
    def process_json(self, line):
        result = [[] for i in range(1,6)]
        data = ujson.loads(line)
        top = 10
        end = len(data["user_info"]["hist_cate"])
        start = 0 if end < top else end - top
        result[0].append([xxhash.xxh64_intdigest(data["user_info"]["hist_cate"][i] + "1") for i in range(start, end)])#laststring-10
        result[1].append([xxhash.xxh64_intdigest(data["user_info"]["hist_subcate"][i] + "2") for i in range(start, end)])#laststring-10
        result[2].append([xxhash.xxh64_intdigest(data["item_info"][0]["nid_cate"] + "3")])
        result[3].append([xxhash.xxh64_intdigest(data["item_info"][0]["nid_subcate"] + "4")])
        result[4].append([int(data["item_info"][0]["click"])])
        return zip([i for i in ["f_hist_cate", "f_hist_subcate", "f_nid_cate",
            "f_nid_subcate","f_click"]], result)

    def test_jsonfile2prototxt(self):
        from utils import json2proto, compile_proto, jsonfile2prototxt

        with open("./mergelog-1.json") as f:
            line = f.read()
        line = ujson.loads(line.strip())
        json2proto(line, "rank")

        jsonfile2prototxt("mergelog-100.json", "rank.proto", line_num = 10, start_part = 1)

    def test_extract_records_result(self):

        from feature_extractor import FeatureExtractor
        from utils import json2proto

        with open("./mergelog-1.json") as f:
            line = f.read()
        line = ujson.loads(line.strip())
        json2proto(line, "rank")

        fe = FeatureExtractor()
        fe.build("./conf/slot_list.conf", "rank.proto")

        start = time.time()
        dataset = fe.parse_proto_file("./mergelog.prototxt")
        result = []
        #test
        for request in dataset:
            result.append(fe.extract_from_records(request))
        end = time.time()

        print("{} .ms".format((end - start) * 1000))

        with open("./mergelog-100.json") as f:
            for idx,line in enumerate(f.readlines()):
                #print(result[idx].items())
                #print(self.process_json(line))
                assert(result[idx].items() == self.process_json(line))

    def test_extract_records_pair_result(self):

        from feature_extractor import FeatureExtractor
        from utils import json2proto

        with open("./mergelog-1.json") as f:
            line = f.read()
        line = ujson.loads(line.strip())
        json2proto(line, "rank")

        fe = FeatureExtractor()
        fe.build("./conf/slot_list.conf", "rank.proto")

        start = time.time()
        dataset = fe.parse_proto_file("./mergelog.prototxt")
        result = []
        #test
        for request in dataset:
            result.append(fe.extract_from_records_pair(
                user_info=request.user_info, item_info=request.item_info))
        end = time.time()

        print("{} .ms".format((end - start) * 1000))

        with open("./mergelog-100.json") as f:
            for idx,line in enumerate(f.readlines()):
                #print(result[idx].items())
                #print(self.process_json(line))
                assert(result[idx].items() == self.process_json(line))

    def test_extract_json_result(self):
        from feature_extractor import FeatureExtractor
        
        fe = FeatureExtractor()
        fe.build("./conf/slot_list.conf")

        start = time.time()
        result = []
        with open("./mergelog-100.json") as f:
            for idx,line in enumerate(f.readlines()):
                result.append(fe.extract_from_json(line))
        end = time.time()
        print("{} .ms".format((end - start) * 1000))

        with open("./mergelog-100.json") as f:
            for idx, line in enumerate(f.readlines()):
                assert(result[idx].items() == self.process_json(line))

if __name__ == "__main__":
    unittest.main()
