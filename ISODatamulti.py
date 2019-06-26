import numpy
import math
import random
import gdal
'''
K = 8#初始类别数（期望）
TN = 20#每个类别中样本最小数目
TS = 1#每个类别的标准差
TC = 0.5#每个类别间的最小距离
L = 5#每次允许合并的最大类别对的数量
I = 10#迭代次数
'''
class Pixel:
    """Pixel"""
    def __init__(self, initY: int, initX: int, initColor):
        self.x = initX
        self.y = initY
        self.color = initColor

class Cluster:
    """Cluster in Gray"""
    def __init__(self, initCenter):
        self.center = initCenter
        self.pixelList = []

class ClusterPair:
    """Cluster Pair"""
    def __init__(self, initClusterAIndex: int, initClusterBIndex: int, initDistance):
        self.clusterAIndex = initClusterAIndex
        self.clusterBIndex = initClusterBIndex
        self.distance = initDistance
def distanceBetween(colorA, colorB) -> float:
  
    dR = int(colorA[0]) - int(colorB[0])
    dG = int(colorA[1]) - int(colorB[1])
    dB = int(colorA[2]) - int(colorB[2])
    dN = int(colorA[3]) - int(colorB[3])
    return math.sqrt((dR**2)+(dG**2)+(dB**2)+(dN**2))
  


def ISOData(dataset, K=4, TN=20, TS=1.0, TC=0.5, L=3, I=1):   
    K=int(K)
    TN=int(TN)
    L=int(L)
    I=int(I)
    im_bands = dataset.RasterCount #波段数
    imgX = dataset.RasterXSize #栅格矩阵的列数
    imgY = dataset.RasterYSize #栅格矩阵的行数
    im_geotrans = dataset.GetGeoTransform()  #仿射矩阵
    im_proj = dataset.GetProjection() #地图投影信息
    imgArray = dataset.ReadAsArray(0,0,imgX,imgY)#获取数据
    
    clusterList = []
    # 随机生成聚类中心
    for i in range(0, K):
        randomX = random.randint(0, imgX - 1)
        randomY = random.randint(0, imgY - 1)
        duplicated = False
        for cluster in clusterList:
            if (cluster.center[0] == imgArray[0,randomY,randomX] and
                cluster.center[1] == imgArray[1,randomY,randomX] and
                cluster.center[2] == imgArray[2,randomY,randomX] and
                cluster.center[3] == imgArray[3,randomY,randomX]
                ):
                duplicated = True
                break
        if not duplicated:
            clusterList.append(Cluster(numpy.array([imgArray[0,randomY,randomX],
                                                    imgArray[1,randomY,randomX],
                                                    imgArray[2,randomY,randomX],
                                                    imgArray[3,randomY,randomX],
                                                    ])))

    # 开始迭代
    iterationCount = 0
    didAnythingInLastIteration = True
    while True:
        iterationCount += 1

        # 清空每一类内像元
        for cluster in clusterList:
            cluster.pixelList.clear()
        print("------")
        print("迭代第{0}次".format(iterationCount))

        #将所有像元分类
        print("分类...", end = '', flush = True)
        for row in range(0, imgX):
            for col in range(0, imgY):
                targetClusterIndex = 0
                targetClusterDistance = distanceBetween(imgArray[:,col,row], clusterList[0].center)
                # 分类
                for i in range(0, len(clusterList)):
                    currentDistance = distanceBetween(imgArray[:,col,row], clusterList[i].center)
                    if currentDistance < targetClusterDistance:
                        targetClusterDistance = currentDistance
                        targetClusterIndex = i
                clusterList[targetClusterIndex].pixelList.append(Pixel(col, row, imgArray[:,col,row]))
        print(" 结束 ")
        
        #检查类中样本个数是否满足要求
        gotoNextIteration = False
        for i in range(len(clusterList) - 1, -1, -1):
            if len(clusterList[i].pixelList) < TN:
                # 重新分类
                clusterList.pop(i)
                gotoNextIteration = True
                break
        if gotoNextIteration:
            print("样本个数不满足要求")
            continue
        print("样本个数满足要求")
        
        # 重新计算聚类中心
        print("重新计算聚类中心...", end = '', flush = True)
        for cluster in clusterList:
            sumR = 0.0
            sumG = 0.0
            sumB = 0.0
            sumN = 0.0
           
            for pixel in cluster.pixelList:
                sumR += int(pixel.color[0])
                sumG += int(pixel.color[1])
                sumB += int(pixel.color[2])
                sumN += int(pixel.color[3])
            aveR = round(sumR / len(cluster.pixelList))
            aveG = round(sumG / len(cluster.pixelList))
            aveB = round(sumB / len(cluster.pixelList))
            aveN = round(sumN / len(cluster.pixelList))
            
            if (aveR != cluster.center[0] and
                aveG != cluster.center[1] and
                aveB != cluster.center[2] and
                aveN != cluster.center[3]
                ):
                didAnythingInLastIteration = True
            cluster.center = numpy.array([aveR, aveG, aveB, aveN])
        print("结束")
        if iterationCount > I:
            break
        if not didAnythingInLastIteration:
            print("更多迭代次数是不是必要的")
            break

        # 计算平均距离
        print("准备合并或分裂...", end = '', flush = True)
        aveDisctanceList = []
        sumDistanceAll = 0.0
        for cluster in clusterList:
            currentSumDistance = 0.0
            for pixel in cluster.pixelList:
                currentSumDistance += distanceBetween(pixel.color, cluster.center)
            aveDisctanceList.append(float(currentSumDistance) / len(cluster.pixelList))
            sumDistanceAll += currentSumDistance
        aveDistanceAll = float(sumDistanceAll) / (imgX * imgY)
        print(" 结束")

        if (len(clusterList) <= K / 2) or not (iterationCount % 2 == 0 or len(clusterList) >= K * 2):
            # 分裂
            print("开始分裂", end = '', flush = True)
            beforeCount = len(clusterList)
            for i in range(len(clusterList) - 1, -1, -1):
                currentSD = [0.0, 0.0, 0.0, 0.0]
                for pixel in clusterList[i].pixelList:
                    currentSD[0] += (int(pixel.color[0]) - int(clusterList[i].center[0])) ** 2
                    currentSD[1] += (int(pixel.color[1]) - int(clusterList[i].center[1])) ** 2
                    currentSD[2] += (int(pixel.color[2]) - int(clusterList[i].center[2])) ** 2
                    currentSD[3] += (int(pixel.color[3]) - int(clusterList[i].center[3])) ** 2
            
                currentSD[0] = math.sqrt(currentSD[0] / len(clusterList[i].pixelList))
                currentSD[1] = math.sqrt(currentSD[1] / len(clusterList[i].pixelList))
                currentSD[2] = math.sqrt(currentSD[2] / len(clusterList[i].pixelList))
                currentSD[3] = math.sqrt(currentSD[3] / len(clusterList[i].pixelList))
               
                # 计算各波段最大标准差
                # Find the max in SD of R, G, B, N
                maxSD = currentSD[0]
                for j in (1, 2):
                    maxSD = currentSD[j] if currentSD[j] > maxSD else maxSD
                if (maxSD > TS) and ((aveDisctanceList[i] > aveDistanceAll and len(clusterList[i].pixelList) > 2 * (TN + 1)) or (len(clusterList) < K / 2)):
                    gamma = 0.5 * maxSD
                    clusterList[i].center[0] += gamma
                    clusterList[i].center[1] += gamma
                    clusterList[i].center[2] += gamma
                    clusterList[i].center[3] += gamma
                  
                    clusterList.append(Cluster(numpy.array([clusterList[i].center[0],
                                                            clusterList[i].center[1],
                                                            clusterList[i].center[2],
                                                            clusterList[i].center[3]
                                                            ])))
                    clusterList[i].center[0] -= gamma * 2
                    clusterList[i].center[1] -= gamma * 2
                    clusterList[i].center[2] -= gamma * 2
                    clusterList[i].center[3] -= gamma * 2
                    
                    clusterList.append(Cluster(numpy.array([clusterList[i].center[0],
                                                            clusterList[i].center[1],
                                                            clusterList[i].center[2],
                                                            clusterList[i].center[3],
                                                            ])))
                    clusterList.pop(i)
            print(" {0} -> {1}".format(beforeCount, len(clusterList)))
        elif (iterationCount % 2 == 0) or (len(clusterList) >= K * 2) or (iterationCount == I):
            # 合并
            print("合并:", end = '', flush = True)
            beforeCount = len(clusterList)
            didAnythingInLastIteration = False
            clusterPairList = []
            for i in range(0, len(clusterList)):
                for j in range(0, i):
                    currentDistance = distanceBetween(clusterList[i].center, clusterList[j].center)
                    if currentDistance < TC:
                        clusterPairList.append(ClusterPair(i, j, currentDistance))

            clusterPairListSorted = sorted(clusterPairList, key = lambda clusterPair: clusterPair.distance)
            newClusterCenterList = []
            mergedClusterIndexList = []
            mergedPairCount = 0
            for clusterPair in clusterPairList:
                hasBeenMerged = False
                for index in mergedClusterIndexList:
                    if clusterPair.clusterAIndex == index or clusterPair.clusterBIndex == index:
                        hasBeenMerged = True
                        break
                if hasBeenMerged:
                    continue
                newCenterR = int((len(clusterList[clusterPair.clusterAIndex].pixelList) * float(clusterList[clusterPair.clusterAIndex].center[0]) + len(clusterList[clusterPair.clusterBIndex].pixelList) * float(clusterList[clusterPair.clusterBIndex].center[0])) / (len(clusterList[clusterPair.clusterAIndex].pixelList) + len(clusterList[clusterPair.clusterBIndex].pixelList)))
                newCenterG = int((len(clusterList[clusterPair.clusterAIndex].pixelList) * float(clusterList[clusterPair.clusterAIndex].center[1]) + len(clusterList[clusterPair.clusterBIndex].pixelList) * float(clusterList[clusterPair.clusterBIndex].center[1])) / (len(clusterList[clusterPair.clusterAIndex].pixelList) + len(clusterList[clusterPair.clusterBIndex].pixelList)))
                newCenterB = int((len(clusterList[clusterPair.clusterAIndex].pixelList) * float(clusterList[clusterPair.clusterAIndex].center[2]) + len(clusterList[clusterPair.clusterBIndex].pixelList) * float(clusterList[clusterPair.clusterBIndex].center[2])) / (len(clusterList[clusterPair.clusterAIndex].pixelList) + len(clusterList[clusterPair.clusterBIndex].pixelList)))
                newCenterN = int((len(clusterList[clusterPair.clusterAIndex].pixelList) * float(clusterList[clusterPair.clusterAIndex].center[3]) + len(clusterList[clusterPair.clusterBIndex].pixelList) * float(clusterList[clusterPair.clusterBIndex].center[3])) / (len(clusterList[clusterPair.clusterAIndex].pixelList) + len(clusterList[clusterPair.clusterBIndex].pixelList)))
                                
                newClusterCenterList.append([newCenterR, newCenterG, newCenterB,newCenterN])
                mergedClusterIndexList.append(clusterPair.clusterAIndex)
                mergedClusterIndexList.append(clusterPair.clusterBIndex)
                mergedPairCount += 1
                if mergedPairCount > L:
                    break
            if len(mergedClusterIndexList) > 0:
                didAnythingInLastIteration = True
            mergedClusterIndexListSorted = sorted(mergedClusterIndexList, key = lambda clusterIndex: clusterIndex, reverse = True)
            for index in mergedClusterIndexListSorted:
                clusterList.pop(index)
            for center in newClusterCenterList:
                clusterList.append(Cluster(numpy.array([center[0], center[1], center[2],center[3]])))
            print(" {0} -> {1}".format(beforeCount, len(clusterList)))

    # 生成新的图像矩阵
    print("分类结束")
    print("一共分为 {0} 类.".format(len(clusterList)))
    newImgArray = numpy.zeros((4,imgY, imgX), dtype = numpy.uint8)
    for cluster in clusterList:
        for pixel in cluster.pixelList:
            newImgArray[0,pixel.y, pixel.x] = int(cluster.center[0])
            newImgArray[1,pixel.y, pixel.x] = int(cluster.center[1])
            newImgArray[2,pixel.y, pixel.x] = int(cluster.center[2])
            newImgArray[3,pixel.y, pixel.x] = int(cluster.center[3])

    
    
    a2 = numpy.ones((imgY,imgX,3), dtype=numpy.uint8)  
    

    unic = numpy.unique(newImgArray[0])
    color = []
    print("对各个类别进行颜色渲染...")
    for i in range(len(unic)): 
        color.append([random.randint(0, 128),random.randint(0, 255),random.randint(128, 255)])


    for i in range(imgY):
        for j in range(imgX):
            for k in range(len(unic)):
                if(newImgArray[0,i,j] == unic[k]):
                    a2[i,j,0] = color[k][0]
                    a2[i,j,1] = color[k][1]
                    a2[i,j,2] = color[k][2]
    return a2        