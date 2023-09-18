import numpy as np 
import cv2
import base64

def resize(img, shape):
    return cv2.resize(img, shape)

def scale(img):
    return (img / 127.5)  - 1.

def make_square_with_padding(img):
    w = img.width
    h = img.height
    c = 3
    diff = h - w
    if diff > 0:
        pad = np.zeros(shape=(h, diff, c), dtype=np.uint8)
        img = np.concatenate((img, pad), axis=1)
    else :
        pad = np.zeros(shape=(np.abs(diff), w, c), dtype=np.uint8)
        img = np.concatenate((img, pad), axis=0)
    return img

def image_preprocessing(img, input_shape=None):
    img = make_square_with_padding(img)
    if input_shape:
        h, w = input_shape
        img = resize(img, (w, h))
    img = scale(img)
    return img
    
def parse_image(img, shape): 
    img = image_preprocessing(img, shape)
    return img

def parse_result(kpts, shape):
    h, w = shape
    if h < w:
        div = w
    else :
        div = h
    kpts = (kpts / 224) * div
    return kpts.reshape(26,2)

def parse_vertex(vertex):
    xyz = vertex.split(" ")[1:]
    res = [np.float(xyz[0]), np.float(xyz[1]), np.float(xyz[2])]
    return res