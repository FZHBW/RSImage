import numpy as np
arr = np.array([[[1, 1, 1, 134, 45], [3, 46, 45, 65, 3], [23424, 234, 12, 12, 3]],[[1, 1, 1, 134, 45], [3, 46, 45, 65, 3], [23424, 234, 12, 12, 3]],[[1, 1, 1, 134, 45], [3, 46, 45, 65, 3], [23424, 234, 12, 12, 3]]])
print(np.where((arr > 3)&(arr<546)))
print(arr[np.where((arr > 3)&(arr<546))])
temp=np.where((arr > 3)&(arr<546),(arr-2)*3,0)
print(temp)

print(arr)
