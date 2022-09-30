from tkinter import Y
import matplotlib.pyplot as plt
import mcareader as mca
import numpy as np
from scipy.signal import find_peaks

def smooth_ewma(data, alpha): #EWMA data smoothing
    smooth_data = [0]*len(data)
    s0 = data[0]
    for i, ent in enumerate(data):
        if(i==0): 
            smooth_data[i] = s0
        else:
            smooth_data[i] = alpha*ent + (1-alpha)*smooth_data[i-1]
    return smooth_data

def findMaxPeak(energy, peaks):
    max = -1
    maxind = -1
    for i,data in enumerate(energy[peaks]):
        if data>max: 
            max = data
            maxind = i
    return max, maxind

spec1 = mca.Mca("pitchblende2.mca")
spec2 = mca.Mca("bkg_pb2.mca")



# print(spec1.get_calibration_points())
# print(spec2.get_calibration_points())

x1 = spec1.get_points()[0]
y1 = spec1.get_points()[1]
x2 = spec2.get_points()[0]#Same as x1 with the right calibration
y2 = spec2.get_points()[1]


ysub = y1/float(spec1.get_variable("Live Time"))-y2/float(spec2.get_variable("Live Time"))


# y1 = np.append(y1, 0)
# x1 = np.append(x1, 0)
# ysub = y1/float(spec1.get_variable("Live Time"))-y2/float(spec2.get_variable("Live Time"))
smoothd = np.array(smooth_ewma(ysub, 0.5))
# peaks,_= find_peaks(smoothd, distance=500, height = 50)
# maxpeak,_ = findMaxPeak(x1, peaks)

# peaks,_= find_peaks(ysub, distance=300)

# peaks, _ = find_peaks(ysub, height=0.01)


# print(ysub)
# print(ysub[peaks])

# plt.plot(x1, y1/float(spec1.get_variable("Live Time")), 'r', label = "pb Sig")
# plt.plot(x1, y2/float(spec2.get_variable("Live Time")), 'b', label = "Bkg")
# print(maxpeak)
# plt.plot(x1, ysub, 'g', label = "Noisy Data")
plt.plot(x1, smoothd, 'r', label = "Smooth Data" )
lines = [63, 89, 127, 193, 249, 301, 358, 613, 668, 770, 1120, 1235, 1722, 1757, 1840]
for en in lines:
    plt.axvline(x=en, color = 'c', linestyle='dashed', label = "Compton Edge, {} keV".format(en))
# # plt.plot(x1[peaks], smoothd[peaks], 'bx', label = "Peaks identified")
# # plt.plot(x1, smoothd, 'r', label = "Smooth Data")
# plt.legend()
plt.ylim([0,200])
plt.xlim([0,2000])
plt.title("Pitchblend Data")
plt.xlabel("Energy (keV)")
plt.ylabel("Counts/sec")
plt.savefig("Pitchblend.png")
# plt.show()