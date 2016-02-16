import numpy as np
import ctypes
import matplotlib.pyplot as plt

n = 100
mu = 0
sig = 0.1
x = np.random.normal(mu,sig,100)
print x
m = 0
v = 0
s = 0
k = 0

stats = ctypes.cdll.LoadLibrary("./stats.so")
xptr = x.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
stats.stats(xptr, n, m, v, s, k)
print 'mean = %d, variance = %d, skew = %d, kurtosis = %d' (m, v, s, k)

count, bins, ignored = plt.hist(x, 7, normed=True)
plt.plot(bins, 1/(sig * np.sqrt(2 * np.pi)) * np.exp(-(bins-mu)**2 / (2*sig**2)))
plt.show()
