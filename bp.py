#系统操作库导入(进行文件打开删除)
import os
import threading
#图形与界面操作库导入
import cv2 as cv
from osgeo import gdal
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#数学运算库导入
import numpy as np
import math as m
import My_First_numerical as MFN

class BP_identify:
      #打开文件
      def __init__(self,Path):
            #基本数据准备
            self.network = MFN.seperate_numerical()
            self.x_train=np.loadtxt(Path)
            Path1=Path.replace('x_','t_')
            self.t_train=np.loadtxt(Path1)
            self.train()

      def train(self):
            iters_num = 100000  # 适当设定循环的次数
            train_size = self.x_train.shape[0]
            batch_size = 300
            learning_rate = 0.001

            train_loss_list = []
            train_acc_list = []
            test_acc_list = []
            train_acc=0
            iter_per_epoch = max(train_size / batch_size, 1)

            for i in range(iters_num):
                  batch_mask = np.random.choice(train_size, batch_size)
                  x_batch = self.x_train[batch_mask]
                  t_batch = self.t_train[batch_mask]
    
            # 计算梯度
                  grad = self.network.gradient(x_batch, t_batch)
    
            # 更新参数
                  for key in ('W1', 'b1', 'W2', 'b2'):
                        self.network.params[key] -= learning_rate * grad[key]
    
                  loss = self.network.loss(x_batch, t_batch)
    
                  if i % iter_per_epoch == 0:
                        train_acc = self.network.accuracy(self.x_train, self.t_train)
                        print("train acc=" + str(train_acc))
                  
                  if train_acc >0.95:
                        break
            print('Basic Caculation Finished')

      def seperate(self,im_BIPArray):
            showimg=im_BIPArray.copy()
            color=[0,0,0]
            for tx in range(0,showimg.shape[0]):
                  for ty in range(0,showimg.shape[1]):
                        t=np.argmax(self.network.predict((showimg[tx,ty,:]).reshape(1,4)), axis=1)[0] 
                        if t==0:
                              color[1]=255
                        elif t==1:
                              color[0]=255
                        elif t==2:
                              color[2]=255
                        showimg[tx,ty,0:3]=color
                        color=[0,0,0]
            return showimg[:,:,0:3]
