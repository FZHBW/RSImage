import numpy as np

def fmake(xyarray,n):
    if xyarray.shape[0]<((n+1)*n/2):
        return np.zeros_like(xyarray)
    else:
        af=np.ones((n,1))
        ab=np.ones((n,1))
        for i in range(1,n):
            for j in range(0,i+1):
                af=np.append(af,(np.power(xyarray[:,0],i-j)*np.power(xyarray[:,1],j)).reshape(xyarray.shape[0],1),axis=1)
                ab=np.append(ab,(np.power(xyarray[:,2],i-j)*np.power(xyarray[:,3],j)).reshape(xyarray.shape[0],1),axis=1)
        return af,ab
        
def fbsolve(xyarray,af,ab,n):
    if xyarray.shape[0]<((n+1)*n/2):
        return np.zeros_like(xyarray)
    elif xyarray.shape[0]==((n+1)*n/2):
        answerfx = np.linalg.solve(af,xyarray[:,2])
        answerfy = np.linalg.solve(af,xyarray[:,3])
        answerbx = np.linalg.solve(ab,xyarray[:,0])
        answerby = np.linalg.solve(ab,xyarray[:,1])
        return answerfx,answerfy,answerbx,answerby
    else:
        answerfx = np.linalg.solve(np.dot(af.T,af),\
                    np.dot(xyarray[:,2].T,xyarray[:,2]))
        answerfy = np.linalg.solve(np.dot(af.T,af),\
                    np.dot(xyarray[:,3].T,xyarray[:,2]))
        answerfx = np.linalg.solve(np.dot(ab.T,ab),\
                    np.dot(xyarray[:,0].T,xyarray[:,0]))
        answerfx = np.linalg.solve(np.dot(ab.T,ab),\
                    np.dot(xyarray[:,1].T,xyarray[:,1]))
        return answerfx,answerfy,answerbx,answerby

def cacu_coordinate(changearray,pointarray,n):
    a1=np.array([1])
    for i in range(1,n):
            for j in range(0,i+1):
                a1=np.append(a1,(np.power(pointarray[0],i-j)*np.power(pointarray[1],j)),axis=1)
    
    