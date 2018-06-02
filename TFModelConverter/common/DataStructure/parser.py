import numpy as np
import common.IR.graph_pb2 as graph_pb2
from common.IR.graph_pb2 import NodeDef, GraphDef, DataType

class Parser(object):
    def __init__(self):
        self.IR_graph=GraphDef()
        self.weight_loaded=False
        self.weights=dict()
    def run(self,dest_path):
        self.gen_IR()
        self.save_to_json(dest_path+'.json')
        self.save_to_proto(dest_path+'.pb')
        self.save_to_weights(dest_path+'.npy')

    @property
    def src_graph(self):
        raise NotImplementedError

    def get_son(self,name,path,set_flag=False):
        return self.src_graph.get_son(name, path, set_flag)
    def get_parent(self, name, path, set_flag = False):
        return self.src_graph.get_parent(name, path, set_flag)

    def set_weight(self,layer_name,weight_name,data):
        if not layer_name in self.weights:
            self.weights[layer_name]=dict()
        layer=self.weights[layer_name]
        layer[weight_name]=data
    def save_to_json(self,filename):
        import google.protobuf.json_format as json_format
        json_str=json_format.MessageToJson(self.IR_graph,preserving_proto_field_name=True)
        with open(filename,'w') as of:
            of.write(json_str)
        print("IR network structure is saved as [{}].".format(filename))
        return json_str
    def save_to_proto(self,filename):
        proto_str=self.IR_graph.SerializeToString()
        with open(filename,'wb') as of:
            of.write(proto_str)
        print("IR network structure is saved as [{}].".format(filename))
        return proto_str
    def save_weights(self,filename):
        if self.weight_loaded:
            with open(filename,'wb') as of:
                np.save(of,self.weights)
            print("IR weights are saved as [{}].".format(filename))
        else:
            print("Warning: weights are not loaded.")