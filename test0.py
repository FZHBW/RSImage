import numpy as np
'''
#arr0 = np.array([[1, 1], [1, 134], [3, 46], [45, 65], [234, 12], [12, 3]])
#arr1=np.array([[1, 1, 1, 134, 45], [3, 46, 45, 65, 3], [23424, 234, 12, 12, 3]])
#arr2=np.array([[1, 1, 1, 134, 45], [3, 46, 45, 65, 3], [23424, 234, 12, 12, 3]])

x1=np.array([0,102,102])
y1=np.array([102,0,102])

x=np.array([x1,y1])

x2=np.array([0,112,112])
y2=np.array([12,0,112])
y=np.array([x2,y2])
'''
xyarray=np.loadtxt('/Users/huangyh/Documents/PythonLearning/RSImage/points.txt')
a0=np.ones((xyarray.shape[0],1))
for i in range(1,4):
            for j in range(0,i+1):
                a0=np.append(a0,(np.power(xyarray[:,0],i-j)*np.power(xyarray[:,1],j)).reshape(xyarray.shape[0],1),axis=1)
                print(a0)
print(a0)