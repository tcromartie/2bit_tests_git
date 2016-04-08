import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt
plt.rc('text', usetex=False)

filename = 'guppi_55179_GBNCC06605_0045_short.fits'
hdu = fits.open(filename,memmap=True)
data = hdu[1].data
z = np.squeeze(data[0]['DATA']).T

# BANDPASS MEAN PLOT
zmean = z.mean(axis=1)
band = np.arange(0,len(zmean),1)
poly = np.polyfit(band,zmean,2)
polyeq = np.zeros(len(zmean))
for i in range(len(zmean)):
    polyeq[i] = poly[2] + poly[1]*band[i] + poly[0]*band[i]**2.

plt.clf()
fig = plt.figure(1)
ax = fig.add_subplot(411)
ax.plot(band,zmean)
ax.plot(band,polyeq,'k')
ax.set_ylim(0,255)
plt.ylabel('Avg value over all timeslices')
plt.title('%s'%(filename))

# RANGE OF TIME BINS:
bins = np.arange(3000,3005,1)
ax3 = fig.add_subplot(412)
for i in range(len(bins)):
        ax3.plot(band,z[:,bins[i]],label='timeslice = %i'%(bins[i]))
plt.legend(fontsize=8)
ax3.plot(band,polyeq,'k')
ax3.set_ylim(0,255)
#plt.xlabel(r'channels')

# SINGLE TIME BIN:
bin = 4000
ax2 = fig.add_subplot(413)
ax2.plot(band,z[:,bin],label='timeslice = %i'%(bin))
plt.legend(fontsize=8)
plt.xlabel(r'channels')
ax2.set_ylim(0,255)
ax2.plot(band,polyeq,'k')
#plt.ylabel(r'single time bin = %i'%(bin))
plt.show()

#targetmean = 1.5
#targetstdev = 0.8
znorm = np.zeros((len(z),len(z[0,:])))
zscoff = np.zeros((len(z),len(z[0,:])))
chanav = np.zeros(len(z))
chanstdev = np.zeros(len(z))
TESTRANGEL = 0
TESTRANGEH = len(z)
count = 0
STD_count = 0
for i in range(TESTRANGEL,TESTRANGEH):
    chanav[i] = np.mean(z[i,:])
    chanstdev[i] = np.std(z[i,:])
    if (chanstdev[i] == 0.0):
        chanstdev[i] = 0.000001
        STD_count = STD_count + 1.
    for j in range(0,len(z[0,:])):  
        znorm[i,j] = (z[i,j]-chanav[i])/chanstdev[i]
        zscoff[i,j] = znorm[i,j]*0.25 + 1.5
        if (zscoff[i,j] > 4.):
                zscoff[i,j] = 4.
                count = count + 1.
        if (zscoff[i,j] < 0.):
                zscoff[i,j] = 0.
                count = count + 1.
print 'Overflow fraction = %i/%i, STD_count (stdev=0-->0.000001) = %i/%i' %(count,i,STD_count,i)

ax7 = fig.add_subplot(414)
ax7.set_ylim(0,4)
bins2 = np.arange(TESTRANGEL,TESTRANGEH)
for k in range(len(bins2)):
    ax7.plot(band,zscoff[:,bins2[k]])
