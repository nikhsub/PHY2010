import enum
from tkinter import Y
from turtle import width
import matplotlib.pyplot as plt
import mcareader as mca
import numpy as np
import math

def peak_counts(x1, x2, y1, y2):
    ysub = y1-y2
    peakind = [False, -1]
    peaklow = [False, -1]
    peakhigh = [False, -1]
    for i, en in enumerate(x1):
        if(not peakind[0]):
            if(en>=peak_en and en<=peak_en+peak_width/2):
                peakind[1] = i
                peakind[0] = True

        if(not peaklow[0]):
            if(en>=peak_en-peak_width/2):
                peaklow[1] = i
                peaklow[0] = True

        if(not peakhigh[0]):
            if(en>=peak_en+peak_width/2):
                peakhigh[1] = i
                peakhigh[0] = True

    totcounts = 0
    for x in range(peaklow[1], peakhigh[1]):
        totcounts+= ysub[x]
    
    return totcounts

spec1 = mca.Mca("")
spec2 = mca.Mca("")
cut_en = 488
cut_ind = -1

peak_en = 1332
peak_width = 24

x1 = spec1.get_points()[0]
y1 = spec1.get_points()[1]
x2 = spec2.get_points()[0]
y2 = spec2.get_points()[1]

y2 = y2*(float(spec1.get_variable("Live Time"))/float(spec2.get_variable("Live Time")))

y=y1-y2


peak = round(peak_counts(x1, x2, y1, y2))

plt.plot(x1, y, 'r', label = "")
plt.legend()
plt.ylim([0,5000])
plt.xlim([0, 2000])
plt.xlabel("Energy (keV)")
plt.ylabel("Counts")
plt.title("")
plt.figtext(0.65, 0.74, f"peak1 = {peak}")
plt.figtext(0.65, 0.62, f"sigma1 = {round(math.sqrt(peak),2)}")
plt.show()
