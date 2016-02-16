import numpy as np
import ctypes
import matplotlib.pyplot as plt

n = 10000
mu = 0
sig = 0.1
x = np.random.normal(mu,sig,n).astype(np.float32)
print x
m = ctypes.c_double()
v = ctypes.c_double()
s = ctypes.c_double()
k = ctypes.c_double()

stats = ctypes.cdll.LoadLibrary("./stats.so")
xptr = x.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

stats.stats(xptr, n, ctypes.byref(m),ctypes.byref(v), ctypes.byref(s), ctypes.byref(k))
print 'mean = %f, variance = %f, skew = %f, kurtosis = %f' %(m.value, v.value, s.value, k.value)

count, bins, ignored = plt.hist(x, 50, normed=True)
plt.plot(bins, 1/(sig * np.sqrt(2 * np.pi)) * np.exp(-(bins-mu)**2 / (2*sig**2)))
plt.show()
