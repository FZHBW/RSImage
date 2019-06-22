import os
from tkinter import Tk ,filedialog
import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from osgeo import gdal
from PIL import Image, ImageTk

class RSImage:
      #打开文件
      def __init__(self,filename):
            #基本数据准备
            self.dataset = gdal.Open(filename)#文件打开
            self.PT=[]#样本存储矩阵
            self.Average=[]#均值矩阵
            self.Variance=[]#协方差矩阵
            self.fig=plt.figure('RGBImage')#窗体名称
            self.n=0#总样本点个数
            self.each_P=[]#每类点个数
            self.num_of_POI=0#总样本点个数
            self.showimg=np.array([])
            
            #临时变量准备
            self.PTb=[]#每类样本点临时数组
            self.teach_KP=0#每类的样本点个数
            
            #获取文件基本信息
            self.im_width = self.dataset.RasterXSize #栅格矩阵的列数
            self.im_height = self.dataset.RasterYSize #栅格矩阵的行数
            self.im_bands = self.dataset.RasterCount #波段数
            self.im_geotrans = self.dataset.GetGeoTransform()#获取仿射矩阵信息
            self.im_proj = self.dataset.GetProjection()#获取投影信息 
            for b in range(self.dataset.RasterCount):
                  # 注意GDAL中的band计数是从1开始的
                  band = self.dataset.GetRasterBand(b + 1)
                  # 波段数据的一些信息
                  print(f'数据类型：{gdal.GetDataTypeName(band.DataType)}')  # DataType属性返回的是数字
                  print(f'NoData值：{band.GetNoDataValue()}')  # 很多影像都是NoData，我们在做数据处理时要特别对待
                  print(f'统计值（最大值最小值）：{band.ComputeRasterMinMax()}')  # 有些数据本身就存储了统计信息，有些数据没有需要计算

            
            #获取数据
            self.im_data = self.dataset.ReadAsArray(0,0,self.im_width,self.im_height)#将读取的数据作为
            self.operate_data=self.im_data.copy()#拷贝一份数据避免原数据被损坏
            self.LinearStretch()
            print('hello')


      def get_BIPImage(self):
            
            #从数据中提取波段
            im_BIPArray=np.append(\
                  self.operate_data[2,0:self.im_height,0:self.im_width].reshape(self.im_height*self.im_width,1),\
                  self.operate_data[1,0:self.im_height,0:self.im_width].reshape(self.im_height*self.im_width,1),axis=1)#合并红绿波段

            im_BIPArray=np.append(im_BIPArray,\
                  self.operate_data[0,0:self.im_height,0:self.im_width].reshape(self.im_height*self.im_width,1),axis=1)#合并红绿蓝波段

            Max0=np.max(im_BIPArray)
            Min0=np.min(im_BIPArray)
            im_BIPArray=im_BIPArray-Min0
            
            k=255/(Max0-Min0)
            im_BIPArray=im_BIPArray*k
            im_BIPArray=im_BIPArray.reshape(self.im_height,self.im_width,3)#调整图像尺寸
            return im_BIPArray

      def LinearStretch(self):
            self.Historydata=np.array([])
            for i in range(0,self.im_bands):     
                  first_edge, last_edge = self.operate_data[:,:,i].min(), self.operate_data[:,:,i].max()
                  n_equal_bins = last_edge-first_edge
                  self.Historydata=np.append(self.Historydata,np.histogram(self.operate_data[:,:,i].flatten(),bins=n_equal_bins,range=(first_edge,last_edge)))
            print('123')

