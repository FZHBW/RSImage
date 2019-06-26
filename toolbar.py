# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolbar.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from osgeo import gdal
import numpy as np 
from PIL import Image
import cv2
import os
import sys
import FileOpen as FO

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuBaisc = QtWidgets.QMenu(self.menubar)
        self.menuBaisc.setObjectName("menuBaisc")
        self.menuChoice = QtWidgets.QMenu(self.menubar)
        self.menuChoice.setObjectName("menuChoice")
        self.menuAdvanced = QtWidgets.QMenu(self.menubar)
        self.menuAdvanced.setObjectName("menuAdvanced")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionFilter = QtWidgets.QAction(MainWindow)
        self.actionFilter.setObjectName("actionFilter")
        self.actionEnhancemen = QtWidgets.QAction(MainWindow)
        self.actionEnhancemen.setObjectName("actionEnhancemen")
        self.actionHistogramMatch = QtWidgets.QAction(MainWindow)
        self.actionHistogramMatch.setObjectName("actionHistogramMatch")
        self.actionGeoCorrection = QtWidgets.QAction(self.menuBaisc)
        self.actionGeoCorrection.setObjectName("actionGeoCorrection")
        self.actionPCA = QtWidgets.QAction(MainWindow)
        self.actionPCA.setObjectName("actionPCA")
        self.actionLinear = QtWidgets.QAction(MainWindow)
        self.actionLinear.setCheckable(True)
        self.actionLinear.setObjectName("actionLinear")
        self.actionDouble = QtWidgets.QAction(MainWindow)
        self.actionDouble.setCheckable(True)
        self.actionDouble.setObjectName("actionDouble")
        self.actionClassify_ISOData = QtWidgets.QAction(MainWindow)
        self.actionClassify_ISOData.setObjectName("actionClassify_ISOData")
        self.actionEdge = QtWidgets.QAction(MainWindow)
        self.actionEdge.setObjectName("actionEdge")
        self.actionFouri = QtWidgets.QAction(MainWindow)
        self.actionFouri.setObjectName("actionFouri")
        self.actionSeperate = QtWidgets.QAction(MainWindow)
        self.actionSeperate.setObjectName("actionSeperate")

        
        

        self.menuBaisc.addAction(self.actionOpen)
        self.menuBaisc.addAction(self.actionFilter)
        self.menuBaisc.addAction(self.actionEnhancemen)
        self.menuBaisc.addAction(self.actionHistogramMatch)
        self.menuBaisc.addAction(self.actionPCA)
        self.menuBaisc.addAction(self.actionGeoCorrection)
        self.menuBaisc.addAction(self.actionClassify_ISOData)
        self.menuChoice.addAction(self.actionEdge)
        self.menuChoice.addAction(self.actionFouri)
        self.menuAdvanced.addAction(self.actionSeperate)
        self.menubar.addAction(self.menuBaisc.menuAction())
        self.menubar.addAction(self.menuChoice.menuAction())
        self.menubar.addAction(self.menuAdvanced.menuAction())
    
        self.actionOpen.triggered.connect(self.Imgopen)
        self.actionEnhancemen.triggered.connect(self.Enhancemen)
        self.actionPCA.triggered.connect(self.PCA)
        self.actionFilter.triggered.connect(self.filter)
        self.actionHistogramMatch.triggered.connect(self.diagrammatch)
        self.actionClassify_ISOData.triggered.connect(self.ISO)
        self.actionSeperate.triggered.connect(self.BPNet)
        self.actionGeoCorrection.triggered.connect(self.graphiccorrectr)
        self.retranslateUi(MainWindow)
        self.cwd = os.getcwd()


        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuBaisc.setTitle(_translate("MainWindow", "Baisc"))
        self.menuChoice.setTitle(_translate("MainWindow", "Choice"))
        self.menuAdvanced.setTitle(_translate("MainWindow", "Advanced"))
        self.actionGeoCorrection.setText(_translate("MainWindow", "GeoCorrection"))
        self.actionEnhancemen.setText(_translate("MainWindow", "Enhancemen"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionFilter.setText(_translate("MainWindow", "Filter"))
        self.actionHistogramMatch.setText(_translate("MainWindow", "HistogramMatch"))
        self.actionPCA.setText(_translate("MainWindow", "PCA"))
        self.actionLinear.setText(_translate("MainWindow", "Linear"))
        self.actionDouble.setText(_translate("MainWindow", "Double"))
        self.actionClassify_ISOData.setText(_translate("MainWindow", "Classify(ISOData)"))
        self.actionEdge.setText(_translate("MainWindow", "Edge"))
        self.actionFouri.setText(_translate("MainWindow", "Fourier"))
        self.actionSeperate.setText(_translate("MainWindow", "Seperate"))

    def Imgopen(self):
        filepath,filetype=QtWidgets.QFileDialog.getOpenFileName\
            (MainWindow,caption="文件打开",directory=self.cwd,filter="Tif File(*.tif)")
        print(filepath)
        self.img=FO.RSImage(filepath)
        imgarr=self.img.getshowimg(self.img.get_BIPImage(self.img.im_data))
        self.showimg(imgarr,self.img.im_width,self.img.im_height)
        print("Opened")

    def showimg(self,imgarr,im_width,im_height):
        imgarr=imgarr.astype(np.uint8)
        imgarr=imgarr.flatten()
        qImg=QtGui.QImage(imgarr.tobytes(),im_width, im_height, im_width*3, QtGui.QImage.Format_RGB888)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addPixmap(QtGui.QPixmap.fromImage(qImg))
        self.graphicsView.setScene(graphicscene)

    def Enhancemen(self):
        self.showimg(self.img.getshowimg(self.img.stretcharr),self.img.im_width,self.img.im_height)

    def PCA(self):
        self.showimg(self.img.getshowimg(self.img.PCAChange(3)),self.img.im_width,self.img.im_height)

    def filter(self):
        filepath,filetype=QtWidgets.QFileDialog.getOpenFileName\
            (MainWindow,caption="文件打开",directory=self.cwd,filter="TXT File(*.txt)")
        self.showimg(self.img.getshowimg(self.img.get_BIPImage(self.img.ConvFilter(filepath))),self.img.im_width,self.img.im_height)

    def diagrammatch(self):
        filepath,filetype=QtWidgets.QFileDialog.getOpenFileName\
            (MainWindow,caption="文件打开",directory=self.cwd,filter="tif File(*.tif)")
        self.showimg(self.img.getshowimg(self.img.get_BIPImage(self.img.DiagrameMatch(filepath))),self.img.im_width,self.img.im_height)

    def ISO(self):
        filepath,filetype=QtWidgets.QFileDialog.getOpenFileName\
            (MainWindow,caption="文件打开",directory=self.cwd,filter="txt File(*.txt)")
        self.showimg(self.img.ISODataSeperator(filepath),(self.img.im_width),(self.img.im_height))

    def BPNet(self):
        filepath,filetype=QtWidgets.QFileDialog.getOpenFileName\
            (MainWindow,caption="点数据文件打开",directory=self.cwd,filter="TXT File(*.txt)")
        self.showimg(self.img.BpSeperate(filepath),self.img.im_width,self.img.im_height)

    def graphiccorrectr(self):
        filepath1,filetype=QtWidgets.QFileDialog.getOpenFileName\
            (MainWindow,caption="基础信息文件打开",directory=self.cwd,filter="TXT File(*.txt)")
        filepath2,filetype=QtWidgets.QFileDialog.getOpenFileName\
            (MainWindow,caption="控制点文件打开",directory=self.cwd,filter="TXT File(*.txt)")
        temp=self.img.get_BIPImage(self.img.Geometric_correction(filepath1, filepath2))
        temp=np.where(temp==0,temp+1024,temp)
        self.showimg(self.img.getshowimg(temp),self.img.new_im_width+1,self.img.new_im_heigth+1)
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


