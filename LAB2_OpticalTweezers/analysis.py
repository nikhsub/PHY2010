from cgitb import grey
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d # Allow 3D surface plots
import math as mt
import time
# To save images as a movie
import io
import cv2                       # Video processor
# import skimage                     # Image processor
# from PIL import Image

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
    for i in range(1, len(centx)):
        dist = mt.sqrt((centx[i]-centx[i-1])**2+(centy[i]-centy[i-1])**2)
        dists.append(dist)
    return dists, sum(dists)

def smooth_ewma(data, alpha): #EWMA data smoothing
    smooth_data = [0]*len(data)
    s0 = data[0]
    for i, ent in enumerate(data):
        if(i==0): 
            smooth_data[i] = s0
        else:
            smooth_data[i] = alpha*ent + (1-alpha)*smooth_data[i-1]
    return smooth_data
        

vidfiles = ['2mw_1710_cropped.mp4', '4mw_1710_cropped.mp4', '6mw_1710_cropped.mp4', '8mw_1710_cropped.mp4', '10mw_1710_cropped.mp4', '19mw_1710_cropped.mp4']
allframes = []
for file in vidfiles:
    vidcap = cv2.VideoCapture(file)
    frames = []
    for i in range(100):
        success, frame = vidcap.read()
        greyframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(greyframe)
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
dist2mw, sum2 = distFromPrev(cent2mwx, cent2mwy)
dist4mw, sum4 = distFromPrev(cent4mwx, cent4mwy)
dist6mw, sum6 = distFromPrev(cent6mwx, cent6mwy)
dist8mw, sum8 = distFromPrev(cent8mwx, cent8mwy)
dist10mw, sum10 = distFromPrev(cent10mwx, cent10mwy)
dist19mw, sum19 = distFromPrev(cent19mwx, cent19mwy)

# smoothdist2 = smooth_ewma(dist2mw, 0.05)
# smoothdist4 = smooth_ewma(dist4mw, 0.05)
# smoothdist6 = smooth_ewma(dist6mw, 0.05)
# smoothdist8 = smooth_ewma(dist8mw, 0.05)
# smoothdist10 = smooth_ewma(dist10mw, 0.05)
# smoothdist19 = smooth_ewma(dist19mw, 0.05)

# plt.plot(x, smoothdist2, label = "2mw")
# plt.plot(x, smoothdist4, label = "4mw")
# plt.plot(x, smoothdist6, label = "6mw")
# plt.plot(x, smoothdist8, label = "8mw")
# plt.plot(x, smoothdist10, label = "10mw")
# plt.plot(x, smoothdist19, label = "19mw")
# plt.xlabel("Frames")
# plt.ylabel("Change in center")
power = [2, 4, 6, 8, 10, 19]
fluc = [sum2,sum4, sum6, sum8, sum10, sum19]
plt.scatter(power, fluc)
plt.legend()
plt.show()





