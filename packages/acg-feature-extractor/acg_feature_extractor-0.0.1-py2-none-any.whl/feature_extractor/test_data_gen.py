from feature_extractor import FeatureExtractor
import paddle.fluid.incubate.data_generator as dg
import sys

class ProtoData(dg.MultiSlotDataGenerator):
    def __init__(self, conf_file, data_path):
        self.fe = FeatureExtractor()
        self.fe.build(conf_file, "rank.proto")
        self.data_path = data_path
        self.batch_size_ = 4
        self._proto_info=None

    def generate_sample(self,line):
        def data_iter():
            dataset = self.fe.parse_proto_file(self.data_path + line.strip())
            for record in dataset:
                result_dict = self.fe.extract_from_records(record)
                result = [(key,result_dict[key][0]) for key in result_dict]
                yield result
        return data_iter

#head -n 1 data/prototxt/file_list.txt | python test_data_gen.py data/prototxt/
data_path = sys.argv[1]
data_gen = ProtoData("./conf/slot_list.conf", data_path)
data_gen.run_from_stdin()
