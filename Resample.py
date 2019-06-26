import numpy as np
import math

def Nearest(img,x,y):
    return img[:,int(y),int(x)]

def Bilinear(img,src_x,src_y):
    src_x0 = int(np.floor(src_x))
    src_x1 = min(src_x0 + 1 ,img.shape[2] - 1)
    src_y0 = int(np.floor(src_y))
    src_y1 = min(src_y0 + 1, img.shape[1] - 1)

    temp0 = (src_x1 - src_x) * img[:,src_y0,src_x0] + (src_x - src_x0) * img[:,src_y0,src_x0]
    temp1 = (src_x1 - src_x) * img[:,src_y1,src_x0] + (src_x - src_x0) * img[:,src_y1,src_x1]
    return (src_y1 - src_y) * temp0+(src_y - src_y0) * temp1
    