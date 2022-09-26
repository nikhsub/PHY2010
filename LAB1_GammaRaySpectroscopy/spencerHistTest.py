import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson

data = pd.DataFrame({'hist_test':np.random.poisson(5,100)})
binwidth = 1
xstart = 0
xend = 10
bins = np.arange(xstart,xend,binwidth)


np.histogram(data, bins='auto')


mu = data["hist_test"].mean() 
n = len(data)

plt.plot(bins + binwidth/2 , n*(poisson.cdf(bins+binwidth,mu) - poisson.cdf(bins,mu)), color='red')

plt.hist(data, bins='auto')
plt.title("hist_test")
plt.figtext(0.15, 0.83, f"mean: {mu}")
plt.figtext(0.15, 0.78, f"total: {n}")
plt.show()
