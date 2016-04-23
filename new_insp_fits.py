import numpy as np
from astropy.io import fits
from matplotlib import pyplot as plt
import scipy.stats

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
ax = fig.add_subplot(511)
ax.plot(band,zmean)
ax.plot(band,polyeq,'k')
ax.set_ylim(0,255)
plt.ylabel('Avg val. over time')
plt.title('%s'%(filename))

# RANGE OF TIME BINS:
bins = np.arange(3000,3005,1)
ax3 = fig.add_subplot(512)
for i in range(len(bins)):
        ax3.plot(band,z[:,bins[i]],label='timeslice = %i'%(bins[i]))
plt.legend(fontsize=8)
ax3.plot(band,polyeq,'k')
ax3.set_ylim(0,255)

# SINGLE TIME BIN:
bin = 4000
ax2 = fig.add_subplot(513)
ax2.plot(band,z[:,bin],label='timeslice = %i'%(bin))
plt.legend(fontsize=8)
plt.xlabel(r'channels')
ax2.set_ylim(0,255)
ax2.plot(band,polyeq,'k')
plt.show()

############## DOF CALCULATIONS ################
# SCOTT'S APRIL 9 ADDITIONAL SUGGESTIONS:
d = np.squeeze(hdu[1].data['DATA'])
t = d[0].T  # this is the first row of data, transposed
ss = scipy.stats.skew(t, axis=1)  # the skewnesses of all the channels
ks = scipy.stats.kurtosis(t, axis=1)  # the kurts of all channels
# The following two compute the effective number of DOFs from the skewness and kurtosis of the central 2096 channels (throwing out the lowest and highest 1000 channels
DOF_SKEW = 8.0/(ss[1000:-1000].mean())**2.0
DOF_KURT = 12./ks[1000:-1000].mean()
DOF_SKEW_ALL = 8.0/(ss)**2.0
print "Effective DOF from skew = %f, from kurtosis = %f" %(DOF_SKEW,DOF_KURT)
################################################

# NOW FOR *NEW* CLIPPING:
up_clip = scipy.stats.chi2.ppf(0.01,np.ceil(DOF_SKEW))
low_clip = scipy.stats.chi2.ppf(0.99,np.ceil(DOF_SKEW))
################################################

znorm = np.zeros((len(z),len(z[0,:])))
zscoff = np.zeros((len(z),len(z[0,:])))
chanav = np.zeros(len(z))
chanstdev = np.zeros(len(z))
TESTRANGEL = 0
TESTRANGEH = 1000
count = 0
STD_count = 0
# uses middle half of data to figure out representative mean
red_factor = np.mean(DOF_SKEW)/np.mean(zmean[len(band)/4.:3.*len(band)/4])

for i in range(TESTRANGEL,TESTRANGEH):
    chanav[i] = np.mean(z[i,:])
    chanstdev[i] = np.std(z[i,:])
    if (chanstdev[i] == 0.0):
        # THIS SHOULD BE SET WEIGHT = 0 IN C CODE
        chanstdev[i] = 0.000001
        STD_count = STD_count + 1.
    for j in range(0,len(z[0,:])):  
        znorm[i,j] = (z[i,j]-chanav[i])/chanstdev[i]
        zscoff[i,j] = (znorm[i,j]*(red_factor)) + 1.
        
# OLD CLIPPING METHOD:
        if (zscoff[i,j] > 4.):
                #zscoff[i,j] = 4.
                count = count + 1.
        if (zscoff[i,j] < 0.):
                #zscoff[i,j] = 0.
                count = count + 1.

print 'Overflow fraction = %i/%i, STD_count (stdev=0-->0.000001) = %i/%i' %(count,(i-TESTRANGEL),STD_count,(i-TESTRANGEL))

################################################
# MAKE YOUR FINAL PLOT OF THE RESCALED, OFFSET & CLIPPED DATA:
ax7 = fig.add_subplot(514)
ax7.set_ylim(-1,5)
bins2 = np.arange(TESTRANGEL,TESTRANGEH)
for k in range(len(bins2)):
    ax7.plot(band,zscoff[:,bins2[k]])
################################################
    
# PLOT DOF FOR EACH CHAN AND CHAN MEAN
ax8 = fig.add_subplot(515)
ax8.plot(band,DOF_SKEW_ALL,label='DOF_SKEW_ALL')
ax8.plot(band,zmean,label='zmean')
#ax8.plot(band,red_factor,label='mean(DOFSKEW)/mean(MEAN)')
ax8.set_ylim(-10,100)
plt.legend()
