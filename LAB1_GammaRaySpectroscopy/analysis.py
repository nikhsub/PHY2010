import matplotlib.pyplot as plt
import mcareader as mca
spec1 = mca.Mca("Co_10cm_1uC.mca")
spec2 = mca.Mca("bkg_without_top_bricks.mca")
# print(spec1.get_calibration_points())
# print(spec2.get_calibration_points())
# print(spec2.raw)
x1 = spec1.get_points()[0]
y1 = spec1.get_points()[1]
x2 = spec2.get_points()[0]
y2 = spec2.get_points()[1]
plt.plot(x1, y1/float(spec1.get_variable("Live Time")), 'r', label = "Co Sig")
plt.plot(x2, y2/float(spec2.get_variable("Live Time")), 'b', label = "Bkg")
plt.plot(x1, y1/float(spec1.get_variable("Live Time"))-y2/float(spec2.get_variable("Live Time")), 'g', label = "Sig-Bkg")
plt.legend()
plt.ylim([0,0.10])
plt.xlim([200, 2400])
plt.xlabel("Energy (keV)")
plt.ylabel("Counts/sec")
plt.savefig("present.png")


#Subtract after cutting out unimportant bins or before?
#Does the graph make sense
