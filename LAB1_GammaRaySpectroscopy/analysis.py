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

spec1 = mca.Mca("Co_10cm_1uC.mca")
spec2 = mca.Mca("bkg_no_top_pb.mca")
# print(spec1.get_calibration_points())
# print(spec2.get_calibration_points())
x1 = spec1.get_points()[0]
y1 = spec1.get_points()[1]
x2 = spec2.get_points()[0]#Same as x1 with the right calibration
y2 = spec2.get_points()[1]
ysub = y1/float(spec1.get_variable("Live Time"))-y2/float(spec2.get_variable("Live Time"))
smoothd = np.array(smooth_ewma(ysub, 0.03))
peaks,_= find_peaks(smoothd, distance=300)
# peaks,_= find_peaks(ysub, distance=300)

# peaks, _ = find_peaks(ysub, height=0.01)




# print(ysub)
# print(ysub[peaks])

# plt.plot(x1, y1/float(spec1.get_variable("Live Time")), 'r', label = "Co Sig")
# plt.plot(x2, y2/float(spec2.get_variable("Live Time")), 'b', label = "Bkg")
# plt.plot(x1, ysub, 'g', label = "Noisy Data" )
plt.plot(x1[peaks], smoothd[peaks], 'bx', label = "Peaks identified")
plt.plot(x1, smoothd, 'r', label = "Smooth Data")
plt.legend()
plt.ylim([0,0.008])
plt.xlim([850, 1800])
plt.title("Co60 Calibration Data")
plt.xlabel("Energy (keV)")
plt.ylabel("Counts/sec")
plt.savefig("Smoothdata.png")
# plt.show()