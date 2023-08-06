"""
json to proto
"""
# -*- coding: utf-8 -*-
import os
import sys
import json
import inspect
from grpc_tools import protoc
import six

def dict_parser(*argv, **kwargs):
    """

    Arguments:
    - `*argv`:
    """
    obj = argv[0]
    name = argv[1]
    vname = argv[1]
    _idx = argv[2]
    ks = obj.keys()

    _t = kwargs.get('repeated', 0) and 'repeated' or 'optional'
    sons = ['message %s {' % (name + "_Class", )]
    for idx, k in enumerate(ks):
        sons.append(_par(obj[k], k, idx + 1))
    sons.append('}')
    if _idx:
        sons.append('%s %s %s = %d;' % (_t, name + "_Class", vname, _idx))
    return '\n'.join(sons)

def list_parser(*argv, **kwargs):
    """

    Arguments:
    - `*argv`:
    """
    obj = argv[0]
    name = argv[1]
    vname = argv[1]
    _idx = argv[2]
    _rp = kwargs.get('repeated', 0) and 'repeated' or 'optional'
    if len(obj) < 1:
        return 'optional int32 %s = %d;' % (name, _idx)
    else:
        if _rp == 'repeated':
            rst = _par(obj[0], name + '_node', 1, repeated=1)
            return 'message ' + name + '{\n' + rst + '}\n repeated ' + name + ' ' + vname + ' = %d;' % _idx
        else:
            r = _par(obj[0], name, _idx, repeated=1)
            return r

def other_parser(*argv, **kwargs):
    """

    Arguments:
    - `*argv`:
    """
    obj = argv[0]
    name = argv[1]
    idx = argv[2]
    _tp = kwargs.get('repeated', 0) and 'repeated' or 'required'
    _tp = kwargs.get('repeated', 0) and 'repeated' or 'optional'
    if isinstance(obj, six.integer_types):
        _t = 'int32'
    elif isinstance(obj, float):
        _t = 'float'
    else:
        _t = 'string'
    return '%s %s %s = %d;' % (_tp, _t, name, idx)


def get_parser(obj):
    """

    Arguments:
    - `obj`:
    """
    _t = type(obj)
    _tn = 'other'
    if _t is dict:
        _tn = 'dict'
    elif _t is list:
        _tn = 'list'
    _f = '%s_parser' % (_tn, )
    _m = sys.modules[__name__]
    for _n, _func in  inspect.getmembers(_m):
        if _n == _f:
            return _func
    return None

def _par(*argv, **kwargs):
    """

    Arguments:
    - `obj`:
    """
    obj = argv[0]
    name = argv[1]
    idx = argv[2]
    _f = get_parser(obj)
    return _f(obj, name, idx, **kwargs)

def json2proto(json_sample, proto_name):
    """
    json to proto
    """
    output = "syntax = \"proto2\";\n" + "package rank_pb;\n"
    output += "message Dataset {\nrepeated Msg_Class msg = 1;\n}\n"

    output += _par(json_sample, "Msg", 0)
    with open("{}.proto".format(proto_name), "w") as f:
        f.write(output)

def compile_proto(proto_file_path):
    """
    compile proto
    """
    proto_file_name = os.path.split(proto_file_path)[1]
    if not os.path.exists(proto_file_name):
        os.system("cp {} .".format(proto_file_path))
    protoc.main(('',
        '-I.',
        '--python_out=.',
        '--grpc_python_out=.',
        proto_file_name))


if __name__ == '__main__':
    _c = ''
    with open(sys.argv[1], 'r') as f:
        _c = f.read()
        f.close()
    obj = json.loads(_c)
    obk = {'a': 'ba',
           'b': [1, 2, 3],
           'c': {"a1": 1},
           'd': [[{'a': 1}]],
           'e': [{'e1': 'e2'}]}
    json2proto(obj, "rank")
    compile_proto("rank.proto")
