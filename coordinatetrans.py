import numpy as np

def fmake(xyarray,n):
    if xyarray.shape[0]<((n+1)*n/2):
        return np.zeros_like(xyarray)
    else:
        af=np.zeros((xyarray.shape[0],1))
        ab=np.zeros((xyarray.shape[0],1))
        for i in range(0,n+1):
            for j in range(0,i+1):
                af=np.append(af,(np.power(xyarray[:,0],i-j)*np.power(xyarray[:,1],j)).reshape(xyarray.shape[0],1),axis=1)
                ab=np.append(ab,(np.power(xyarray[:,2],i-j)*np.power(xyarray[:,3],j)).reshape(xyarray.shape[0],1),axis=1)
        af=np.delete(af,0,axis=1)
        ab=np.delete(ab,0,axis=1)
        return af,ab
        
def fbsolve(xyarray,n):
    af,ab=fmake(xyarray,n)
    if xyarray.shape[0]<((n+2)*(n+1)/2):
        return np.zeros_like(xyarray)
    elif xyarray.shape[0]==((n+2)*(n+1)/2):
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

def cacu_coordinatea(changearrayx,changearrayy,pointarray,n):
    a1=np.zeros((pointarray.shape[0],1))
    changearrayx=changearrayx.reshape(1,changearrayx.shape[0])
    changearrayy=changearrayy.reshape(1,changearrayy.shape[0])
    for i in range(0,n+1):
            for j in range(0,i+1):
                a1=np.append(a1,(np.power(pointarray[:,0],i-j)*np.power(pointarray[:,1],j)).reshape(pointarray.shape[0],1),axis=1)
    a1=np.delete(a1,0,axis=1)
    a1=a1.T
    point=np.array([np.dot(changearrayx,a1),np.dot(changearrayy,a1)]).reshape(pointarray.shape[0],2)
    return point
    
def cacu_coordinate(changearrayx,changearrayy,nx,ny,n):
    a1=np.array([])
    for i in range(0,n+1):
            for j in range(0,i+1):
                a1=np.append(a1,(np.power(nx,i-j)*np.power(ny,j)))
    return np.dot(changearrayx,a1.T),np.dot(changearrayy,a1.T)
    '''
    a1=np.zeros((pointarray.shape[0],1))
    changearrayx=changearrayx.reshape(1,changearrayx.shape[0])
    changearrayy=changearrayy.reshape(1,changearrayy.shape[0])
    for i in range(0,n+1):
            for j in range(0,i+1):
                a1=np.append(a1,(np.power(pointarray[:,0],i-j)*np.power(pointarray[:,1],j)).reshape(pointarray.shape[0],1),axis=1)
    a1=np.delete(a1,0,axis=1)
    a1=a1.T
    point=np.array([np.dot(changearrayx,a1),np.dot(changearrayy,a1)]).reshape(pointarray.shape[0],2)
    return point
    '''