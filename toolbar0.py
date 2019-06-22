# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fileopen.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from tkinter import Tk ,filedialog
import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from osgeo import gdal

class Ui_FileOpen(object):
    def setupUi(self, FileOpen):
        FileOpen.setObjectName("FileOpen")
        FileOpen.resize(430, 66)
        self.pushButton = QtWidgets.QPushButton(FileOpen)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(FileOpen)
        self.comboBox.setGeometry(QtCore.QRect(150, 20, 141, 32))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(FileOpen)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 20, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(FileOpen)
        
        
        QtCore.QMetaObject.connectSlotsByName(FileOpen)

    def retranslateUi(self, FileOpen):
        _translate = QtCore.QCoreApplication.translate
        FileOpen.setWindowTitle(_translate("FileOpen", "Dialog"))
        self.pushButton.setText(_translate("FileOpen", "文件打开"))
        self.comboBox.setItemText(0, _translate("FileOpen", "增强"))
        self.pushButton_2.setText(_translate("FileOpen", "执行"))
        self.pushButton.clicked.connect(self.openimage)


    def openimage(self):
            root = Tk()
            root.withdraw()
            root.update()
            filename = filedialog.askopenfilename(initialdir = 'huangyh')
            root.quit()
            self.dataset = gdal.Open(filename)#文件打开
            self.PT=[]#样本存储矩阵
            self.Average=[]#均值矩阵
            self.Variance=[]#协方差矩阵
            self.fig=plt.figure('RGBImage')#窗体名称
            self.n=0#总样本点个数
            self.each_P=[]#每类点个数
            self.num_of_POI=0#总样本点个数
            self.showimg=np.array([])
            self.Max=0
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
            operate_data=self.im_data#拷贝一份数据避免原数据被损坏
           
            #从数据中提取波段
            self.im_BIPArray=np.append(\
                  operate_data[2,0:self.im_height,0:self.im_width].reshape(self.im_height*self.im_width,1),\
                  operate_data[1,0:self.im_height,0:self.im_width].reshape(self.im_height*self.im_width,1),axis=1)#合并红绿波段

            self.im_BIPArray=np.append(self.im_BIPArray,\
                  operate_data[0,0:self.im_height,0:self.im_width].reshape(self.im_height*self.im_width,1),axis=1)#合并红绿蓝波段

            self.im_BIPArray=np.append(self.im_BIPArray,\
                  operate_data[3,0:self.im_height,0:self.im_width].reshape(self.im_height*self.im_width,1),axis=1)#合并红绿蓝近红外波段
            self.Max=np.max(self.im_BIPArray)
            self.min=np.min(self.im_BIPArray)
            self.im_BIPArray=self.im_BIPArray-self.min
            k=255/(self.Max)#-self.min)
            self.im_BIPArray=self.im_BIPArray*k#归一化

            self.im_BIPArray=self.im_BIPArray.reshape(self.im_height,self.im_width,self.im_bands)#调整图像尺寸

            plt.imshow(self.im_BIPArray[:,:,0:3]/255)#将图像添加到窗口
            plt.show()#图像显示







class myprog(Ui_FileOpen):
    def __init__ (self, dialog):
        Ui_FileOpen.__init__(self)
        self.setupUi(dialog)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()

    test1 = myprog(dialog)
    dialog.show()
sys.exit(app.exec_())