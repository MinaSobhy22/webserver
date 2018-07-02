
from ctypes import *
import math
import random
import os 

from analyze.apps import lib, meta, net,BOX,IMAGE,METADATA,DETECTION

# free_detections = lib.free_detections
# free_detections.argtypes = [POINTER(DETECTION), c_int]

def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res

def detect(net, meta, im, thresh=.5, hier_thresh=.5, nms=.45):
    free_image = lib.free_image
    free_image.argtypes = [IMAGE]

    make_boxes = lib.make_boxes
    make_boxes.argtypes = [c_void_p]
    make_boxes.restype = POINTER(BOX)

    make_probs = lib.make_probs
    make_probs.argtypes = [c_void_p]
    make_probs.restype = POINTER(POINTER(c_float))

    free_ptrs = lib.free_ptrs
    free_ptrs.argtypes = [POINTER(c_void_p), c_int]


    num_boxes = lib.num_boxes
    num_boxes.argtypes = [c_void_p]
    num_boxes.restype = c_int

    network_detect = lib.network_detect
    network_detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]

    boxes = make_boxes(net)
    probs = make_probs(net)
    num =   num_boxes(net)

    network_detect(net, im, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_ptrs(cast(probs, POINTER(c_void_p)), num)
    return res
    

def get_analysis(inputs):
    load_image = lib.load_image_color
    load_image.argtypes = [c_char_p, c_int, c_int]
    load_image.restype = IMAGE

    if ('image_path' in inputs):
        image = load_image(inputs['image_path'], 0, 0)
    else:
        return -1
        
    # net = darknet.load_net("cfg/densenet201.cfg", "/home/pjreddie/trained/densenet201.weights", 0)
    #im = load_image("data/wolf.jpg", 0, 0)
    #meta = load_meta("cfg/imagenet1k.data")
    #r = classify(net, meta, im)
    #print r[:10]

    r = detect(net, meta, image)
    return r

    