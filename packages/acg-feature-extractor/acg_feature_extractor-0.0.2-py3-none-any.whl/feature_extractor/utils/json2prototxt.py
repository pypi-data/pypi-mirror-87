"""
json to prototxt
"""
from __future__ import absolute_import
import sys
import ujson
import os
import importlib

from . import pbjson
from .schema_parse import json2proto, compile_proto

def trans_from_file(file_path, proto_file, line_num=10000, start_part=0):
    """
    json file to prototxt
    """
    compile_proto(proto_file)
    proto_file_name = os.path.split(proto_file)[1]
    proto_module_name = proto_file_name.split(".")[0] + "_pb2"
    rank_pb2 = importlib.import_module(proto_module_name)

    part = start_part
    index = 1
    os.system("mkdir -p prototxt")
    os.system("cp {} prototxt".format(proto_file))
    with open(file_path) as f:
        file_name = os.path.split(file_path)[1]
        request = rank_pb2.Dataset()
        for line in f.readlines():
            msg_ins = pbjson.json2pb(rank_pb2.Msg_Class, line)
            request.msg.append(msg_ins)
            index += 1
            if index < line_num:
                continue
            else:
                with open(
                        "prototxt/" + file_name.split(".")[0] + "-part-{}.prototxt".format(
                        str(part).zfill(5)), "wb") as f:
                    f.write(request.SerializeToString())
                request = rank_pb2.Dataset()
                index = 1
                part += 1
        if index > 1:
            with open("prototxt/" + file_name.split(".")[0] + "-part-{}.prototxt".format(
                str(part).zfill(5)), "wb") as f:
                f.write(request.SerializeToString())

    with open("prototxt/file_list.txt", "w") as f:
        line = ""
        for i in range(part + 1):
            line += file_name.split(".")[0] + "-part-{}.prototxt\n".format(str(i).zfill(5))
        f.write(line)
    return part


# tran json sample to prototxt
if __name__ == "__main__":
   #trans_from_stdin(rank_pb2)
   trans_from_file("../mergelog-100.json", "../rank.proto", line_num=10, start_part=0)
