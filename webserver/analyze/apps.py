# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from ctypes import *
import math
import random
import os 


class AnalyzeConfig(AppConfig):
    name = 'analyze'
    def ready(self):
        global lib, net, meta
        some_data = 3902375

        dir_path = os.path.dirname(os.path.realpath(__file__))
        lib = CDLL(dir_path + "/darknet/libdarknet.so", RTLD_GLOBAL)
        # lib = CDLL("/home/minasobhy/Desktop/webserver/analyze/darknet/libdarknet.so", RTLD_GLOBAL)
        lib.network_width.argtypes = [c_void_p]
        lib.network_width.restype = c_int
        lib.network_height.argtypes = [c_void_p]
        lib.network_height.restype = c_int

        set_gpu = lib.cuda_set_device
        set_gpu.argtypes = [c_int]

        load_net = lib.load_network
        load_net.argtypes = [c_char_p, c_char_p, c_int]
        load_net.restype = c_void_p
        load_meta = lib.get_metadata
        lib.get_metadata.argtypes = [c_char_p]
        lib.get_metadata.restype = METADATA

        rgbgr_image = lib.rgbgr_image
        rgbgr_image.argtypes = [IMAGE]


        net = load_net(dir_path + "/darknet/cfg/yolo.cfg", dir_path + "/darknet/yolo.weights", 0)
        meta = load_meta(dir_path + "/darknet/cfg/coco.data")



def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]
                
class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

    
