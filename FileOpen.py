import os
import math as m
import numpy as np
from osgeo import gdal
import linecache
import coordinatetrans as cd
import Resample as rp
import bp
import ISODatamulti as ISO

class RSImage:
      #打开文件
      def __init__(self,filename):
            #基本数据准备
            self.dataset = gdal.Open(filename)#文件打开
            self.PT=[]#样本存储矩阵
            self.Average=[]#均值矩阵
            self.Variance=[]#协方差矩阵
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
            #self.Geometric_correction('/Users/huangyh/Documents/PythonLearning/RSImage/points.txt')
            print('hello')

      def get_BIPImage(self,imgarr):
            #从数据中提取波段
            im_BIPArray=np.append(\
                  imgarr[2,0:imgarr.shape[1],0:imgarr.shape[2]].reshape(imgarr.shape[1]*imgarr.shape[2],1),\
                  imgarr[1,0:imgarr.shape[1],0:imgarr.shape[2]].reshape(imgarr.shape[1]*imgarr.shape[2],1),axis=1)#合并红绿波段

            im_BIPArray=np.append(im_BIPArray,\
                  imgarr[0,0:imgarr.shape[1],0:imgarr.shape[2]].reshape(imgarr.shape[1]*imgarr.shape[2],1),axis=1)#合并红绿蓝波段
            if imgarr.shape[0]>3:
                  im_BIPArray=np.append(im_BIPArray,\
                        imgarr[3,0:imgarr.shape[1],0:imgarr.shape[2]].reshape(imgarr.shape[1]*imgarr.shape[2],1),axis=1)#合并红绿蓝近红外波段

            im_BIPArray=im_BIPArray.reshape(imgarr.shape[1],imgarr.shape[2],4)#调整图像尺寸
            return im_BIPArray

      def getshowimg(self,im_BIPArray):
            Max0=np.max(im_BIPArray)
            Min0=np.min(im_BIPArray)
            im_BIPArray=im_BIPArray-Min0
            k=255/(Max0-Min0)
            im_BIPArray=(im_BIPArray)*k          
            return im_BIPArray[:,:,0:3]

      def LinearStretch(self):
            self.Historydata=[]
            self.Historyindex=[]
            temparr=self.im_data.copy()
            tempimg=[]
            for i in range(0,self.im_bands):   
                  first_edge, last_edge = np.min(temparr[i,:,:]), np.max(temparr[i,:,:])
                  n_equal_bins = last_edge-first_edge
                  mini,maxi=first_edge,first_edge
                  a=0
                  tempd,tempi=np.histogram(temparr[i,:,:].flatten(),bins=n_equal_bins,range=(first_edge,last_edge),density=True)
                  self.Historydata.append(tempd)
                  self.Historyindex.append(tempi)
                  for j in tempd:
                        a+=j
                        if a<0.01:
                              mini+=1
                              maxi+=1
                        elif a<0.99:
                              maxi+=1
                        elif a>0.99:
                              break    
                  k=n_equal_bins/(maxi-mini)
                  temparr[i,:,:]=np.where((temparr[i,:,:]<maxi)&(temparr[i,:,:]>mini),(temparr[i,:,:]-mini+1)*k,temparr[i,:,:])
            self.Historydata=np.array(self.Historydata)
            self.lHistorydata=np.array(self.Historydata)
            self.Historyindex=np.array(self.Historyindex)
            self.stretcharr=self.get_BIPImage(temparr)
                    
      def PCAChange(self,n):
            self.pcaarr=self.get_BIPImage(self.im_data)#将图像转化为BIP格式便于计算
            cacutemparr=self.pcaarr.reshape(self.im_height*self.im_width,4)#将图像转为m*n的形式
            meanVal=np.mean(cacutemparr,axis=0)#求出图像的均值
            cacutemparr=cacutemparr-meanVal#求出零均值数据
            covx=np.dot(cacutemparr.T,cacutemparr)/(self.im_height*self.im_width)#计算协方差
            self.eigVals,eigVects=np.linalg.eig(covx)#求出特征值以及特征值矩阵
            eigValIndice=np.argsort(-self.eigVals)            #对特征值从小到大排序
            n_eigValIndice=eigValIndice[0:n]   #最大的n个特征值的下标
            self.n_eigVect=eigVects[:,n_eigValIndice]        #最大的n个特征值对应的特征向量
            self.pcaarr=np.dot(self.pcaarr,self.n_eigVect)
            temparr=self.pcaarr
            temparr[:,:,1]=temparr[:,:,0]
            temparr[:,:,2]=temparr[:,:,0]
            return temparr
      
      def DiagrameMatch(self,Path):
            
            reference_dataset=gdal.Open(Path)
            rim_width = reference_dataset.RasterXSize #栅格矩阵的列数
            rim_height = reference_dataset.RasterYSize #栅格矩阵的行数
            rim_data = reference_dataset.ReadAsArray(0,0,rim_width,rim_height)#将读取的数据作为
            a1,a2=0,0

            first_edge, last_edge = np.min(rim_data[0,:,:]), np.max(rim_data[0,:,:])
            n_equal_bins = last_edge-first_edge
            mini,maxi=first_edge,first_edge
            tempd,tempi=np.histogram(rim_data[0,:,:].flatten(),bins=n_equal_bins,range=(first_edge,last_edge),density=True)
            temptempd=np.zeros_like(tempd)
            templhisd=np.zeros_like(self.Historydata)
           
            #计算累计直方图
            self.changedarr=self.operate_data.copy()
            for i in range(0,tempd.shape[0]):
                  a1+=tempd[i]
                  temptempd[i]=a1
                  
            for i in range(0,self.im_bands):
                  a2=0
                  for j in range(0,self.Historydata[i].shape[0]):
                        a2+=self.Historydata[i][j]       
                        tempminus=np.abs(temptempd-a2) 
                        self.changedarr[i,:,:]=np.where((self.operate_data[i,:,:]==self.Historyindex[i][j]),tempi[np.argmin(tempminus)],self.changedarr[i,:,:])
            print('dsfvf')
            return self.changedarr

      def ConvFilter(self,Path):
            filtercore=np.loadtxt(Path)
            filtercore=filtercore.flatten()
            k2=int(filtercore.shape[0])
            k=int((m.sqrt(k2)-1)/2)
            filterarr=np.zeros_like(self.im_data)
            for i in range(k,self.im_height-k):
                  for j in range(k,self.im_width-k):
                        filterarr[:,i,j]=np.dot(self.operate_data[:,i-k:i+k+1,j-k:j+k+1].reshape(self.im_bands,k2),filtercore.T)

            print('ConvFilter')
            return filterarr

      def Geometric_correction(self,Path1,Path2):
            info=np.loadtxt(Path1)
            points=np.loadtxt(Path2)
            n=int(info[0])
            rptype=int(info[1])
            point4=[]
            fx,fy,bx,by=cd.fbsolve(points,n)
            arr0 = np.array([[0, 0], 
                             [0,self.im_height], 
                             [self.im_width, 0],
                             [self.im_width, self.im_height]])
            arr0=arr0.reshape((4,2))
            bandory=cd.cacu_coordinatea(fx,fy,arr0,n)

            self.newsize=np.max(bandory,axis=0)-np.min(bandory,axis=0)
            self.NewImagearray=np.zeros((4,int(self.newsize[1]+1),int(self.newsize[0]+1)))
            self.new_im_heigth=int(self.newsize[1])
            self.new_im_width=int(self.newsize[0])
            if rptype==1:
                  for i in range(0,self.new_im_heigth-1):
                        for j in range(0,self.new_im_width-1): 
                              ox,oy=cd.cacu_coordinate(bx,by,j,i,n)
                              if ox>=0 and oy>=0 and ox<self.im_width and oy<self.im_height:
                                    self.NewImagearray[:,i,j]=rp.Nearest(self.operate_data,ox,oy)
            if rptype==2:
                  for i in range(0,self.new_im_heigth-1):
                        for j in range(0,self.new_im_width-1): 
                              ox,oy=cd.cacu_coordinate(bx,by,j,i,n)
                              if ox>=0 and oy>=0 and ox<self.im_width and oy<self.im_height:
                                    self.NewImagearray[:,i,j]=rp.Bilinear(self.operate_data,ox,oy)
            print('GC')
            return self.NewImagearray

      def ISODataSeperator(self,Path):
            if Path=='':
                  return ISO.ISOData(self.dataset)
            else:
                  info=np.loadtxt(Path)
                  return ISO.ISOData(self.dataset,info[0],info[1],info[2],info[3],info[4],info[5])
            print('sdfd')
      
      def BpSeperate(self,Path):
            Numerical=bp.BP_identify(Path)
            return Numerical.seperate(self.get_BIPImage(self.operate_data))