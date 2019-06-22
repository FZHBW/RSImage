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
        self.menuGeoCorrection = QtWidgets.QMenu(self.menuBaisc)
        self.menuGeoCorrection.setObjectName("menuGeoCorrection")
        self.menuReSample = QtWidgets.QMenu(self.menuGeoCorrection)
        self.menuReSample.setObjectName("menuReSample")
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
        self.actionEnhancemen = QtWidgets.QAction(MainWindow)
        self.actionEnhancemen.setObjectName("actionEnhancemen")
        self.actionHistogramMatch = QtWidgets.QAction(MainWindow)
        self.actionHistogramMatch.setObjectName("actionHistogramMatch")
        self.actionPCA = QtWidgets.QAction(MainWindow)
        self.actionPCA.setObjectName("actionPCA")
        self.actionLinear = QtWidgets.QAction(MainWindow)
        self.actionLinear.setCheckable(True)
        self.actionLinear.setObjectName("actionLinear")
        self.actionDouble = QtWidgets.QAction(MainWindow)
        self.actionDouble.setCheckable(True)
        self.actionDouble.setObjectName("actionDouble")
        self.actionAffineT = QtWidgets.QAction(MainWindow)
        self.actionAffineT.setObjectName("actionAffineT")
        self.actionPoly_Tran = QtWidgets.QAction(MainWindow)
        self.actionPoly_Tran.setObjectName("actionPoly_Tran")
        self.actionClassify_SVM = QtWidgets.QAction(MainWindow)
        self.actionClassify_SVM.setObjectName("actionClassify_SVM")
        self.actionEdge = QtWidgets.QAction(MainWindow)
        self.actionEdge.setObjectName("actionEdge")
        self.actionFouri = QtWidgets.QAction(MainWindow)
        self.actionFouri.setObjectName("actionFouri")
        self.actionSeperate = QtWidgets.QAction(MainWindow)
        self.actionSeperate.setObjectName("actionSeperate")

        self.menuReSample.addAction(self.actionLinear)
        self.menuReSample.addAction(self.actionDouble)
        self.menuGeoCorrection.addAction(self.menuReSample.menuAction())
        self.menuGeoCorrection.addAction(self.actionAffineT)
        self.menuGeoCorrection.addAction(self.actionPoly_Tran)
        self.menuBaisc.addAction(self.actionOpen)
        self.menuBaisc.addAction(self.actionEnhancemen)
        self.menuBaisc.addAction(self.actionHistogramMatch)
        self.menuBaisc.addAction(self.actionPCA)
        self.menuBaisc.addAction(self.menuGeoCorrection.menuAction())
        self.menuBaisc.addAction(self.actionClassify_SVM)
        self.menuChoice.addAction(self.actionEdge)
        self.menuChoice.addAction(self.actionFouri)
        self.menuAdvanced.addAction(self.actionSeperate)
        self.menubar.addAction(self.menuBaisc.menuAction())
        self.menubar.addAction(self.menuChoice.menuAction())
        self.menubar.addAction(self.menuAdvanced.menuAction())
    
        self.actionOpen.triggered.connect(self.Imgopen)
        self.retranslateUi(MainWindow)


        self.cwd = os.getcwd()


        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuBaisc.setTitle(_translate("MainWindow", "Baisc"))
        self.menuGeoCorrection.setTitle(_translate("MainWindow", "GeoCorrection"))
        self.menuReSample.setTitle(_translate("MainWindow", "ReSample"))
        self.menuChoice.setTitle(_translate("MainWindow", "Choice"))
        self.menuAdvanced.setTitle(_translate("MainWindow", "Advanced"))
        self.actionEnhancemen.setText(_translate("MainWindow", "Enhancemen"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionHistogramMatch.setText(_translate("MainWindow", "HistogramMatch"))
        self.actionPCA.setText(_translate("MainWindow", "PCA"))
        self.actionLinear.setText(_translate("MainWindow", "Linear"))
        self.actionDouble.setText(_translate("MainWindow", "Double"))
        self.actionAffineT.setText(_translate("MainWindow", "Affine Trans"))
        self.actionPoly_Tran.setText(_translate("MainWindow", "Poly Trans"))
        self.actionClassify_SVM.setText(_translate("MainWindow", "Classify(SVM)"))
        self.actionEdge.setText(_translate("MainWindow", "Edge"))
        self.actionFouri.setText(_translate("MainWindow", "Fourier"))
        self.actionSeperate.setText(_translate("MainWindow", "Seperate"))

        

    def Imgopen(self):
        print('Hello!')
        filepath,filetype=QtWidgets.QFileDialog.getOpenFileName\
            (MainWindow,caption="文件打开",directory=self.cwd,filter="Tif File(*.tif)")
        print(filepath)
        img=FO.RSImage(filepath)
        imgarr=img.get_BIPImage()
        imgarr=imgarr.astype(np.uint8)
        imgarr=imgarr.flatten()
        self.showimg(imgarr,img.im_width,img.im_height)
        print("opened")

    def showimg(self,imgarr,im_width,im_height):
        qImg=QtGui.QImage(imgarr.tobytes(),im_width, im_height, im_width*3, QtGui.QImage.Format_RGB888)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addPixmap(QtGui.QPixmap.fromImage(qImg))
        self.graphicsView.setScene(graphicscene)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


