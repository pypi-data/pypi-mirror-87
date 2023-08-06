import numpy as np
import math
import matplotlib.pyplot as plt

def Linearreg(xlist, ylist):
    """ Takes two inputs, in list, tuple or arrays and computes a linear regression with method of least squares.
    Returns k, m, such that y = kx + m & maximum deviation. """ #Add the return of std-error and r^2 value
    if not isinstance((xlist, ylist), (np.generic, np.ndarray)):
        if isinstance((xlist, ylist), (list, tuple)):
            xlist, ylist = np.array(xlist), np.array(ylist)
        else:
            raise TypeError("[LinearRegression] Can't make linear fit with given input")
    if len(xlist) < 2:
        raise TypeError("[LinearRegression] Can't make linear fit with given input, add more terms")
    else:
        Line = lambda k,x,m: k * x + m
        try:
            bline = np.ones(len(xlist))
            A = np.array([xlist, bline]).T
            ATA = A.T.dot(A)
            ATY = A.T.dot(ylist)
            ATAInv = np.linalg.inv(ATA)
            KM = ATAInv.dot(ATY)
            Error = [((KM[0] * xlist[i] + KM[1]) - ylist[i]) for i in range(len(xlist)) if len(xlist) == len(ylist)]
            return KM, max(Error)
        except Exception as E:
            raise E
        #Maximum Deviation, not standard deviation

def ForceLinearreg(xlist,ylist):
    """Linear regression that forces through origion."""
    if not isinstance((xlist, ylist), (np.generic, np.ndarray)):
        if isinstance((xlist, ylist), (list, tuple)):
            xlist, ylist = np.array(xlist), np.array(ylist)
        else:
            raise TypeError("[ForceLinearreg] Can't make linear fit with given input")
    if len(xlist) != len(ylist) or len(xlist) < 2 or len(ylist) < 2:
        raise KeyError("[ForceLinearreg] Can't make linear fit with given input")
    else:
        try:
            line = lambda k,x: k * x
            A = np.array([xlist]).T
            ATA = A.T.dot(A)
            ATY = A.T.dot(ylist)
            ATAInv = np.linalg.inv(ATA)
            KM = ATAInv.dot(ATY)
            Error = [(KM * xlist[i] - ylist[i]) for i in range(len(xlist))]
            return KM, max(Error)
        except Exception as E:
            raise E


"""
xlist1 = np.array([1,2,3,4,5,6,7,8,9,10])
ylist1 = np.array([4,6,9,10,12,14,16,18,20,21])
Model = ForceLinearreg(xlist1, ylist1)
print(Model)
plt.plot(xlist1, ylist1, '.', label = "DATA")
plt.plot(xlist1, xlist1 * Model[0], '-', label = "Regression")
plt.legend()
plt.show()
"""
"""
Regression = Linearregression(xlist1, ylist1)

plt.plot(xlist1,ylist1, '.')
plt.plot(xlist1, Regression[0] * xlist1 + Regression[1])
plt.show()
"""
