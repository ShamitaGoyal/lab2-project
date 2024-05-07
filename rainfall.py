# Name: Shamita Goyal
# Lab 2: Data Analysis / Visualization, GUI

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def sizeOfContainer(func):
    """decorates functions which return containers:
        - checks the size of the container and prints it
        - returns the container for the printContainer decorator"""

    def wrapper(*args, **kwargs):
        container = func(*args, **kwargs)
        print(f"From decorator: the number of data points being plotted: {container}.\n")
        return container

    return wrapper


class Rainfall:
    """contains data from the input file and methods to analyze and plot the data"""
    FILE = "sf_rainfall.csv"

    def __init__(self):

        try:
            self.data = np.loadtxt(Rainfall.FILE, delimiter=",")[:-1]
        except IOError:
            raise SystemExit(f"{Rainfall.FILE} could not be opened.")

        self.dCopy = self.data.copy()

        sumR = np.sum(self.data[:, 1:], 1)
        self._maxY, self._maxIn = self.data[np.where(sumR == np.max(sumR))][0, 0], np.max(sumR)
        self._minY, self._minIn = self.data[np.where(sumR == np.min(sumR))][0, 0], np.min(sumR)
        self._medianIn = np.median(sumR)

        self._lowY = self.data[0, 0]
        self._highY = self.data[-1, 0]

    @property
    def get_highestR(self):
        return self._maxY, self._maxIn

    @property
    def get_lowestR(self):
        return self._minY, self._minIn

    @property
    def get_medianR(self):
        return self._medianIn

    @property
    def get_lowY_highY(self):
        return self._lowY, self._highY


    @sizeOfContainer
    def monthlyDist(self):
        """plots the monthly rainfall distribution"""
        self.dCopy.shape = (self.data.shape[0] * self.data.shape[1],)
        self.fig = plt.figure(figsize=(8, 7))
        plt.hist(self.dCopy[self.dCopy < 1800], color="m")
        plt.ylabel("Frequency")
        plt.xlabel("Monthly Rainfall (in inches)")
        plt.title("Monthly Rainfall Distribution")
        plt.grid()
        # plt.show()
        return len(self.dCopy[self.dCopy < 1800])


    @sizeOfContainer
    def avgMonthly(self):
        """plots the average rainfall for each month"""
        avg_rainfall = np.mean(self.data[:, 1:], axis=0)
        months = ["Jan", "Feb", "Mar",
                  "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep",
                  "Oct", "Nov", "Dec"]

        self.fig = plt.figure(figsize=(8, 7))
        plt.bar(months, avg_rainfall, align="center", color="green")
        plt.xlabel("Months")
        plt.ylabel("Average Rainfall (in inches)")
        plt.title("Average Rainfall per Month")
        plt.xticks(rotation=45)
        plt.grid()
        # plt.show()
        return len(avg_rainfall)

    @sizeOfContainer
    def yearlyR(self, startY, endY):
        """plots the yearly rainfall for a range of years, depending on user choice"""
        subsetY = self.data[(self.data >= startY) & (self.data <= endY)]
        subsetD = self.data[(self.data[:, 0] >= startY) & (self.data[:, 0] <= endY), 1:]

        sumD = np.sum(subsetD, 1)
        subsetAvg = np.mean(sumD)

        self.fig = plt.figure(figsize=(8, 7))
        plt.plot(subsetY, sumD, label='Yearly Rainfall')
        plt.plot([startY,endY],[subsetAvg,subsetAvg], color="r",  linestyle="-.", label='Average Yearly Rainfall')
        #plt.axhline(y=subsetAvg, color='r', linestyle="-.", label='Average Yearly Rainfall')
        plt.title("Yearly Rainfall Trend")
        plt.xlabel("Year")
        plt.ylabel("Yearly rainfall (in inches)")
        plt.legend()
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.grid()
        # plt.show()
        return len(subsetY)



#r = Rainfall()
# r.monthlyDist()
# r.avgMonthly()
# r.yearlyR(1850, 2023)
# r.yearlyR(2000, 2013)