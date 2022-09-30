import enum
from tkinter import Y
from turtle import width
import matplotlib.pyplot as plt
import mcareader as mca
import numpy as np

def compton_counts(x1, x2, y1, y2):
    cut_ind = -1
    low_ind = -1
    for i, en in enumerate(x1):
        if(en<=cut_en):continue
        cut_ind = i
        break

    for i, en in enumerate(x1):
        if(en<=comp_low_en):continue
        low_ind = i
        break

    x1_cut = x1[comp_low_en:cut_ind]
    x2_cut = x2[comp_low_en:cut_ind]
    y1_cut = y1[comp_low_en:cut_ind]
    y2_cut = y2[comp_low_en:cut_ind]

    ysub = y1_cut - y2_cut

    totcounts = 0
    for counts in ysub:
        totcounts+=counts

    # plt.plot(x1_cut, y1_cut, label = "sig")
    # plt.plot(x2_cut, y2_cut, label = "bkg")
    # plt.plot(x1, y1-y2)
    # plt.legend()
    # plt.show()

    return totcounts

def peak_counts(x1, x2, y1, y2, peak_en, peak_width):
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




spec1 = mca.Mca("pitchblende2.mca")
spec2 = mca.Mca("bkg_pb2.mca")
cut_en = 488
comp_low_en = 200
peak_ens = [63, 89, 127, 193, 249, 301, 358, 613, 668, 770, 1120, 1235, 1722, 1757, 1840]
peak_width = 24

x1 = spec1.get_points()[0]
y1 = spec1.get_points()[1]
x2 = spec2.get_points()[0]#Same as x1 with the right calibration
y2 = spec2.get_points()[1]

y2 = y2*(float(spec1.get_variable("Live Time"))/float(spec2.get_variable("Live Time")))

ysub = y1 - y2
totcount = 0
for count in ysub:
    totcount+=count

pcounts = []
for en in peak_ens:
    pcounts.append(peak_counts(x1, x2, y1, y2, en, peak_width))

det_eff = []
for count in pcounts:
    det_eff.append(count/totcount)

det_eff = [i*100 for i in det_eff]
plt.scatter(peak_ens, det_eff, color='r')
plt.title("Detector efficiency vs Energy for Pitchblende")
plt.xlabel("Energy (keV)")
plt.ylabel("Detector efficiency")
plt.savefig("DetEffvsEn.png")





# print(float(spec1.get_variable("Live Time"))/float(spec2.get_variable("Live Time")))
# print(spec1.get_variable("Real Time"))
# print(spec2.get_variable("Real Time"))
# print(y1[100], y2[100])



# spec1.plot(background=spec2)


