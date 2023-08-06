import cv2
import numpy as np

def normalize(x, lower, upper):
    _max = x.max()
    _min = x.min()
    factor =  ((upper - lower) + 1e-12)/ ((_max - _min) + 1e-12)
    return (x - _min) * factor + lower

def rescale2d(x, shape):
    return cv2.resize(x.astype('float'), shape)