import numpy as np
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import functools

class GaussianFit:
    def __init__(self, xlist, ylist):
        self.xlist = xlist
        self.ylist = ylist
        self.xlistcal = None
        self.ylistcal = None
        self.PeakValues = []
        self.Counts = []
        self.Sigma = []
        self.Area = []
        self.Mu = []

    def ComputeGaussian(self, index1, index2):
        """Returns a function of which one can plot the gausian fit with; Maximum error is also returned from when performing the fit"""
        try:
            if self.xlistcal.any() == None:
                try:
                    xlist1 = np.array(self.xlist[index1:index2])
                    ylist0 = self.ylist[index1:index2]
                    ylist1 = np.array([[arg + 1] for arg in ylist0])
                except Exception as E:
                    raise E
            else:
                try:
                    xlist1 = np.array(self.xlistcal[index1:index2])
                    ylist0 = self.ylist[index1:index2]
                    ylist1 = np.array([[arg + 1] for arg in ylist0])
                except Exception as E:
                    raise E
        except Exception as E:
            raise E
        if len(xlist1) < 4:
            raise KeyError("[GaussianFit]: Needs more data to performe gaussian fit.")
        else:
            Constant_a = np.ones(len(xlist1))
            line1 = np.ones(len(xlist1))
            MatrixA = np.array([np.ones(len(xlist1)), xlist1, xlist1 ** 2]).T
            MatrixAT = MatrixA.T
            try:
                InverseA = np.linalg.inv(MatrixAT.dot(MatrixA))
                ylist2 = np.log(ylist1)
                ylist3 = MatrixAT.dot(ylist2)
                Constants = InverseA.dot(ylist3)
            except Exception as E:
                raise E
            sigma = np.sqrt(- 1 / (2 * Constants[2]))
            mu = Constants[1] * sigma ** 2
            A = np.exp(Constants[0] + mu ** 2 / (2 * sigma ** 2))
            #print(A, mu, sigma)
            #print('A', r'$\mu$', r'$\sigma$')
            text = np.array([['A', r'$\mu$', r'$\sigma$'], ['Error']])
            function = lambda x: A * np.exp(-(x-mu)**2/(2*sigma**2))
            def CalculateError(xlist, ylist):
                RelativeError = lambda x, y: (np.log(y) - (Constants[0] + Constants[1] * x + Constants[2] * x ** 2 ))
                ErrorValues = [RelativeError(xlist[i],ylist[i]) for i in range(len(xlist)) if len(xlist) == len(ylist)]
                return max(ErrorValues)
            ErrorValue = CalculateError(xlist1, ylist1) #Maxiumum deviation
            self.PlotFit(function, xlist1)
            self.PeakValues.append(mu)
            self.Counts.append(A)
            self.Sigma.append(sigma)
            def RiemanSum(func, a,b):
                h = 0.01
                riearea = []
                while a-10 < b + 10:
                    riearea.append(func(a)*h)
                    a +=h
                return sum(riearea)
            try:
                Peakarea = RiemanSum(function, self.xlistcal[index1], self.xlistcal[index2])
            except:
                try:
                    Peakarea = RiemanSum(function, self.xlist[index1], self.xlist[index2])
                except Exception as E:
                    raise E
            try:
                self.Area.append(Peakarea)
            except Exception as E:
                raise E
            return function, sigma, ErrorValue

    def Calibratedp(self):
        peaklist = self.PeakValues.copy()
        try:
            peaklist = np.array(peaklist) * self.k
            return peaklist
        except Exception as E:
            raise E

    def PlotData(self, title, xlabel, ylabel, xlim = None):
        try:
            plt.plot(self.xlistcal, self.ylist, '-')
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            if xlim != None:
                try:
                    plt.xlim(0, xlim)
                except Exception as E:
                    raise E
            plt.legend()
            plt.show()
        except:
            try:
                plt.plot(self.xlist, self.ylist, '.')
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
                plt.legend()
                plt.title(title)
                plt.show()
            except Exception as E:
                raise E


    def PlotFit(self, function, xlist, res = 1000):
        if not callable(function):
            raise KeyError("[GaussianFit]: Cannot plot the gaussian fit")
        else:
            try:
                plt.plot(self.xlistcal, self.ylist, '.', label = 'Data')
                xranges = np.linspace(xlist[0], xlist[-1], res)
                yvalues = list(map(function, xranges))
                plt.plot(xranges, yvalues, label = 'Regression')
                plt.legend()
                plt.title("Gausian fit")
                plt.show()
            except:
                plt.plot(self.xlist, self.ylist, '.', label = 'Data')
                xranges = np.linspace(xlist[0], xlist[-1], res)
                yvalues = list(map(function, xranges))
                plt.plot(xranges, yvalues, label = 'Regression')
                plt.legend()
                plt.title("Gausian fit")
                plt.show()

    def Calibration(self, func, *args):
        """Just for Alpha lab."""
        try:
            self.k = args[0]
        except:
            pass
        try:
            xlist = np.array(self.xlist.copy())
            ylist = np.array(self.ylist.copy())
        except Exception as E:
            raise E
        """
        if not callable(func):
            raise KeyError("[System]: GaussianFit can't prefome calibration")
        else:
            try:
                self.xlistcal = np.array(list(map(func, xlist)))
            except Exception as E:
                raise E
        """
        try:
            self.xlistcal = xlist * self.k
        except Exception as E:
            raise E

    def CalibratedPeaks(self):
        CalibratedPeaks1 = self.PeakValues.copy()
        CalibratedPeaks2 = np.array(CalibratedPeaks1)
        try:
            return (CalibratedPeaks2 * self.k)
        except Exception as E:
            raise E


"""
xlist1 = np.array([1,2,3,4,5,6,8,9,10])
ylist1 = np.array([2,3,4,7,8,6,5,4,3])
listx2 = np.linspace(-1, 15, 100)
Fitted = Gaussianfit(xlist1, ylist1)
fittedx = list(map(Fitted, listx2))
Data = GaussianFit(xlist1, ylist1)
data = Data.ComputeGausian(0, 9)
print(data)
plt.plot(listx2, fittedx)
plt.plot(xlist1, ylist1, '.', label = "tested values")

plt.show()
"""
