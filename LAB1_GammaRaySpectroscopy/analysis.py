import matplotlib.pyplot as plt
import mcareader as mca
spec = mca.Mca("Co_10cm_1uC.mca")
x = spec.get_points()[0]
y = spec.get_points()[1]
plt.yscale("log")
plt.plot(x,y)
plt.show()
