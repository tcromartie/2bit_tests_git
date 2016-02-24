import numpy as np
import ctypes
import matplotlib.pyplot as plt
import scipy.stats
from astropy.io import fits

hdu = fits.open('guppi_55197_GBNCC08327_0044_0001.fits',memmap=True)
data = hdu[1].data
z = np.squeeze(data[0]['DATA']).T
#print 'Array shape = %f' %(z.shape)

m = ctypes.c_double()
v = ctypes.c_double()
s = ctypes.c_double()
k = ctypes.c_double()

stats = ctypes.cdll.LoadLibrary("./stats.so")

def chan_stats(x,m,v,s,k):
    xptr = x.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    stats_out = stats.stats(xptr, len(z), ctypes.byref(m),ctypes.byref(v), ctypes.byref(s), ctypes.byref(k))
    #print 'mean = %f, variance = %f, skew = %f, kurtosis = %f' %(m.value, v.value, s.value, k.value)
    #print 'expected values: %f, %f, %f, %f' %(mu, sig, scipy.stats.skew(x), scipy.stats.kurtosis(x))
    #norm_kurt = scipy.stats.kurtosistest(x)
    #print norm_kurt
    #count, bins, ignored = plt.hist(x, 500, normed=True)
    #plt.plot(bins, 1/(sig * np.sqrt(2 * np.pi)) * np.exp(-(bins-mu)**2 / (2*sig**2)))
    #plt.show()
    return [m.value, v.value, s.value, k.value] 

istats = np.zeros(len(z))

for i in range(0,len(z)):
    x = z[i,:]
    np.append(istats,chan_stats(x,m,v,s,k))

print istats
print istats[2000]
