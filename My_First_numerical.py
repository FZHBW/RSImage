#系统操作库导入(进行文件打开删除)
import os
import threading
#图形与界面操作库导入
import cv2
from osgeo import gdal
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#数学运算库导入
import numpy as np
import math as m
from collections import OrderedDict

def sigmoid(x):#Sigmoid函数
        return 1 / (1 + np.exp(-x))

def sigmoid_grad(x):#Sigmoid数值求导函数
    return (1.0 - sigmoid(x)) * sigmoid(x)

def softmax(x):#取整函数
    if x.ndim == 2:
        x = x.T
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)
        return y.T 

    x = x - np.max(x) #溢出对策
    return np.exp(x) / np.sum(np.exp(x))


def cross_entropy_error(y, t):
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
        
    # 监督数据是one-hot-vector的情况下，转换为正确解标签的索引
    if t.size == y.size:
        t = t.argmax(axis=1)
             
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size


#Affine层定义
class Affine:

    def __init__(self, W, b):
        self.W =W
        self.b = b
        
        self.x = None
        self.original_x_shape = None
        # 权重和偏置参数的导数
        self.dW = None
        self.db = None

    def forward(self, x):
        # 对应张量
        self.original_x_shape = x.shape
        x = x.reshape(x.shape[0], -1)#将x形式自动设置为n*...
        self.x = x

        out = np.dot(self.x, self.W) + self.b#计算前向传播结果

        return out

    def backward(self, dout):
        dx = np.dot(dout, self.W.T)
        self.dW = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0)
        
        dx = dx.reshape(*self.original_x_shape)  # 还原输入数据的形状（对应张量）
        return dx

#Relu层定义
class Relu:
    def __init__(self):
        self.mask = None

    def forward(self, x):
        self.mask = (x <= 0)
        out = x.copy()
        out[self.mask] = 0

        return out

    def backward(self, dout):
        dout[self.mask] = 0
        dx = dout

        return dx

#Sigmoid层定义
class Sigmoid:
    def __init__(self):
        self.out = None

    def forward(self, x):
        out = sigmoid(x)
        self.out = out
        return out

    def backward(self, dout):
        dx = dout * (1.0 - self.out) * self.out

        return dx

#SoftMax损失函数层定义
class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None
        self.y = None # softmax的输出
        self.t = None # 监督数据

    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)
        
        return self.loss

    def backward(self, dout=1):
        batch_size = self.t.shape[0]
        if self.t.size == self.y.size:  #监督数据是one-hot-vector的情况
            dx = (self.y - self.t) / batch_size
        
        return dx


#构建BP神经网络
class seperate_numerical:
    def __init__(self, input_size=4, hidden_size=1000, output_size=3, weight_init_std=1):
        #各层权重初始化
        self.params = {}
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)

        #生成层
        self.layers = OrderedDict() 
        self.layers['Affine1'] = \
            Affine(self.params['W1'], self.params['b1']) 
        self.layers['Relu1'] = Relu() 
        self.layers['Affine2'] = \
            Affine(self.params['W2'], self.params['b2']) 
        self.lastLayer = SoftmaxWithLoss()

        print('Numerical Net Inicialized')

    def predict(self, x):#预测函数
        for layer in self.layers.values():
            x=layer.forward(x)
        return x

    def loss(self, x, t):#计算损失函数
        y = self.predict(x)

        return self.lastLayer.forward(y,t)
    
    def accuracy(self, x, t):#精度计算函数
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        t = np.argmax(t, axis=1)   
        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy
        
    # x:输入数据, t:监督数据
    def numerical_gradient(self, x, t):
        loss_W = lambda W: self.loss(x, t)
        
        grads = {}
        grads['W1'] = numerical_gradient(loss_W, self.params['W1'])
        grads['b1'] = numerical_gradient(loss_W, self.params['b1'])
        grads['W2'] = numerical_gradient(loss_W, self.params['W2'])
        grads['b2'] = numerical_gradient(loss_W, self.params['b2'])
        
        return grads

    def gradient(self, x, t):
        # forward 
        self.loss(x, t)

        # backward
        dout = 1
        dout = self.lastLayer.backward(dout)
        layers = list(self.layers.values()) 
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)
        # 设定
        grads = {}
        grads['W1'] = self.layers['Affine1'].dW 
        grads['b1'] = self.layers['Affine1'].db 
        grads['W2'] = self.layers['Affine2'].dW 
        grads['b2'] = self.layers['Affine2'].db

        return grads
