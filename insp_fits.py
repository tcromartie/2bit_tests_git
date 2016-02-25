import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt
plt.rc('text', usetex=True)

filename = 'guppi_55197_GBNCC08327_0044_0001.fits'
hdu = fits.open(filename,memmap=True)
data = hdu[1].data
z = np.squeeze(data[0]['DATA']).T

# BANDPASS MEAN PLOT
zmean = z.mean(axis=1)
band = np.arange(0,len(zmean),1)
plt.clf()
fig = plt.figure(1)
ax = fig.add_subplot(311)
ax.plot(band,zmean)
plt.ylabel('Avg value over all samples')
#plt.xlabel(r'channels')
#plt.title(r"$%s$"%(filename))
plt.title('%s'%(filename))

# RANGE OF TIME BINS:
bins = np.arange(3000,3010,1)
ax3 = fig.add_subplot(312)
for i in range(len(bins)):
	ax3.plot(band,z[:,bins[i]],label='channel = %i'%(bins[i]))
plt.legend(fontsize=8)
#plt.xlabel(r'channels')

# SINGLE TIME BIN:
bin = 4000
ax2 = fig.add_subplot(313)
ax2.plot(band,z[:,bin],label='channel = %i'%(bin))
plt.legend(fontsize=8)
plt.xlabel(r'channels')
#plt.ylabel(r'single time bin = %i'%(bin))

plt.show()

