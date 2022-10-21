from cgitb import grey
from cmath import log
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d # Allow 3D surface plots
from scipy.optimize import curve_fit
import math as mt
import time
# To save images as a movie
import io
import cv2                       # Video processor
# import skimage                     # Image processor
from scipy.ndimage import gaussian_filter
from scipy.stats import chisquare

def findCenters(filenum, allframes):
    frames = allframes[filenum]
    centersx = []
    centersy = []
    for frame in frames:
        x_ind = np.where(frame==frame.max())[1]
        y_ind = np.where(frame==frame.max())[0]
        centersx.append(np.average(x_ind))
        centersy.append(np.average(y_ind))
    return np.array(centersx), np.array(centersy)

def distFromPrev(centx, centy):
    dists = []
    distsq = []
    for i in range(1, len(centx)):
        dist = mt.sqrt((centx[i]-centx[i-1])**2+(centy[i]-centy[i-1])**2)
        dists.append(dist)
        distsq.append(dist*dist)
    return dists, sum(dists), float(sum(distsq))/99

def smooth_ewma(data, alpha): #EWMA data smoothing
    smooth_data = [0]*len(data)
    s0 = data[0]
    for i, ent in enumerate(data):
        if(i==0): 
            smooth_data[i] = s0
        else:
            smooth_data[i] = alpha*ent + (1-alpha)*smooth_data[i-1]
    return smooth_data

def fitfunc(x, a, b):
    return (a/(x+b))
        

# vidfiles = ['23_2010_cropped.mp4', '40_2010_cropped.mp4', '61_2010_cropped.mp4', '86_2010_cropped.mp4', '119_2010_cropped.mp4', '192_2010_cropped.mp4']
vidfiles = ['2mw_1710_cropped.mp4', '4mw_1710_cropped.mp4', '6mw_1710_cropped.mp4', '8mw_1710_cropped.mp4', '10mw_1710_cropped.mp4', '19mw_1710_cropped.mp4']
allframes = []
for file in vidfiles:
    vidcap = cv2.VideoCapture(file)
    frames = []
    for i in range(100):
        success, frame = vidcap.read()
        greyframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        filtframe = gaussian_filter(greyframe, sigma = 6)
        frames.append(filtframe)
        # frames.append(greyframe)
    allframes.append(frames)

cent2mwx, cent2mwy = findCenters(0,allframes)
cent4mwx, cent4mwy = findCenters(1,allframes)
cent6mwx, cent6mwy = findCenters(2,allframes)
cent8mwx, cent8mwy = findCenters(3,allframes)
cent10mwx, cent10mwy = findCenters(4,allframes)
cent19mwx, cent19mwy = findCenters(5,allframes)

# plt.plot(cent2mwx, cent2mwy, label="2mw")
# plt.plot(cent4mwx, cent8mwy, label="4mw")
# plt.plot(cent6mwx, cent6mwy, label="6mw")
# plt.plot(cent8mwx, cent8mwy, label="8mw")
# plt.plot(cent10mwx, cent10mwy, label="10mw")
# plt.plot(cent19mwx, cent19mwy, label="19mw")

x = np.linspace(1, 99, 99)
dist2mw, sum2, sumsq2 = distFromPrev(cent2mwx, cent2mwy)
dist4mw, sum4, sumsq4= distFromPrev(cent4mwx, cent4mwy)
dist6mw, sum6, sumsq6= distFromPrev(cent6mwx, cent6mwy)
dist8mw, sum8, sumsq8 = distFromPrev(cent8mwx, cent8mwy)
dist10mw, sum10, sumsq10= distFromPrev(cent10mwx, cent10mwy)
dist19mw, sum19, sumsq19 = distFromPrev(cent19mwx, cent19mwy)

print(sumsq2, sumsq4, sumsq6, sumsq8, sumsq10, sumsq19)

smoothdist2 = smooth_ewma(dist2mw, 0.02)
smoothdist4 = smooth_ewma(dist4mw, 0.02)
smoothdist6 = smooth_ewma(dist6mw, 0.02)
smoothdist8 = smooth_ewma(dist8mw, 0.02)
smoothdist10 = smooth_ewma(dist10mw, 0.02)
smoothdist19 = smooth_ewma(dist19mw, 0.02)

# plt.plot(x, smoothdist2, label = "2.3mw")
# plt.plot(x, smoothdist4, label = "4.0mw")
# plt.plot(x, smoothdist6, label = "6.1mw")
# plt.plot(x, smoothdist8, label = "8.6mw")
# plt.plot(x, smoothdist10, label = "11.9mw")
# plt.plot(x, smoothdist19, label = "19.2mw")
# plt.plot(x, smoothdist2, label = "2mw")
# plt.plot(x, smoothdist4, label = "4mw")
# plt.plot(x, smoothdist6, label = "6mw")
# plt.plot(x, smoothdist8, label = "8mw")
# plt.plot(x, smoothdist10, label = "10mw")
# plt.plot(x, smoothdist19, label = "19mw")
# plt.xlabel("Frames")
# plt.ylabel("Distance moved by center of bead (pix)")
# plt.title("Motion of bead for different powers")
# power = [2.3, 4.0, 6.1, 8.6, 11.9, 19.2]
# power = [2, 4, 6, 8, 10, 19]
# fluc = [sum2,sum4, sum6, sum8, sum10, sum19]
# plt.scatter(power, fluc, label = "Data")
# popt, pcov = curve_fit(fitfunc, power, fluc)
# plt.plot(power, fitfunc(np.array(power), *popt), color = "r",label = "Fit: a=%5.3f, b=%5.3f" % tuple(popt))
# fitvals = fitfunc(np.array(power), *popt)
# fitvalsnorm = [x/sum(fitvals) for x in fitvals]
# flucnorm = [x/sum(fluc) for x in fluc]
# print(chisquare(fitvalsnorm, flucnorm))
# print(sum(fitvals), sum(fluc))
# plt.xlabel("Laser Power (mW)")
# plt.ylabel("Total vibrations (pix)")
# plt.title("Vibrations as a function of Laser Power")
# plt.legend()
# plt.yscale('log')
# plt.savefig("VibvsPower_wfilter_Data2_params.png")
# plt.savefig("BeadMotion_wfilter_Data2.png")
# plt.show()





