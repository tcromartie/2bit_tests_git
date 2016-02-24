import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt

hdu1 = fits.open('guppi_55197_GBNCC08327_0044_0001.fits',memmap=True)
d = hdu1[1].data
print d[0]['DATA'].shape
z = np.squeeze(d[0]['DATA'])
print z.shape
z = z.T
print z.shape
#print z[:,0]
#plt.hist(z.mean(axis=0),50)
#plt.show()
print z1
