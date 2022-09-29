import enum
from tkinter import Y
from turtle import width
import matplotlib.pyplot as plt
import mcareader as mca
import numpy as np

def compton_counts(x1, x2, y1, y2):
    for i, en in enumerate(x1):
        if(en<=cut_en):continue
        cut_ind = i
        break

    x1_cut = x1[:cut_ind]
    x2_cut = x2[:cut_ind]
    y1_cut = y1[:cut_ind]
    y2_cut = y2[:cut_ind]

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




spec1 = mca.Mca("Cs_068uCi_20cm.mca")
spec2 = mca.Mca("bkg_pb2.mca")
cut_en = 488
cut_ind = -1
peak_en = 661
peak_width = 20

x1 = spec1.get_points()[0]
y1 = spec1.get_points()[1]
x2 = spec2.get_points()[0]#Same as x1 with the right calibration
y2 = spec2.get_points()[1]

y2 = y2*(float(spec1.get_variable("Live Time"))/float(spec2.get_variable("Live Time")))

comp = compton_counts(x1, x2, y1, y2)
print(comp)
# peak = peak_counts(x1, x2, y1, y2)
# print(peak/comp)


# print(float(spec1.get_variable("Live Time"))/float(spec2.get_variable("Live Time")))
# print(spec1.get_variable("Real Time"))
# print(spec2.get_variable("Real Time"))
# print(y1[100], y2[100])



# spec1.plot(background=spec2)


