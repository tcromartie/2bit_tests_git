import os.path
import numpy as np
from astropy.io import fits as pyfits

def unpack_4bit(data):                       
    """Unpack 4-bit data that has been read in as bytes.

        Input: 
            data4bit: array of unsigned 4-bit ints packed into
                an array of bytes.

        Output: 
            outdata: unpacked array. The size of this array will 
                be twice the size of the input data.
    """
    first_piece = np.bitwise_and(15,data)
    second_piece = data >> 4
    return np.dstack([first_piece,second_piece]).flatten()

def unpack_2bit(data):
    first_piece = np.bitwise_and(7,data)
    second_piece = data >> 6
    return np.dstack([first_piece,second_piece]).flatten()

class PsrfitsFile(object):
    def __init__(self, psrfitsfn):
        if not os.path.isfile(psrfitsfn):
            raise ValueError("ERROR: File does not exist!\n\t(%s)" % \
                                psrfitsfn)
        self.filename = psrfitsfn
        print 'filename = %s' %(self.filename)
	self.fits = pyfits.open(psrfitsfn, mode='readonly', memmap=True)
	self.header = self.fits[0].header # Primary HDU
	self.nbits = self.fits['SUBINT'].header['NBITS']
        print 'nbits = %f' %(self.nbits)
	self.nchan = self.fits['SUBINT'].header['NCHAN']
        print 'nchan = %f' %(self.nchan)
	self.nsamp_per_subint = self.fits['SUBINT'].header['NSBLK']
        print 'samp per subint = %f' %(self.nsamp_per_subint)
	self.nsubints = self.fits['SUBINT'].header['NAXIS2']
        print 'num subints = %f' %(self.nsubints)
	self.freqs = self.fits['SUBINT'].data[0]['DAT_FREQ'] 
	print self.freqs

    def read_subint(self, isub, apply_weights=True, apply_scales=True, \
                    apply_offsets=True):
        """
        Read a PSRFITS subint from a open pyfits file object.
         Applys scales, weights, and offsets to the data.

             Inputs: 
                isub: index of subint (first subint is 0)
                apply_weights: If True, apply weights. 
                    (Default: apply weights)
                apply_scales: If True, apply scales. 
                    (Default: apply scales)
                apply_offsets: If True, apply offsets. 
                    (Default: apply offsets)

             Output: 
                data: Subint data with scales, weights, and offsets
                     applied in float32 dtype with shape (nsamps,nchan).
        """ 
	subintdata = self.fits['SUBINT'].data[isub]['DATA']
	print np.array(subintdata)
        if self.nbits == 4:
            data = unpack_4bit(subintdata)
        else:
            data = np.array(subintdata)
        if apply_offsets:
            offsets = self.get_offsets(isub)
        else:
            offsets = 0
        if apply_scales:
            scales = self.get_scales(isub)
        else:
            scales = 1
        if apply_weights:
            weights = self.get_weights(isub)
        else:
            weights = 1
        data = data.reshape((self.nsamp_per_subint,self.nchan))
        data_wso = ((data * scales) + offsets) * weights
        return data_wso

    def get_weights(self, isub):
        """Return weights for a particular subint.

            Inputs:
                isub: index of subint (first subint is 0)
            
            Output:
                weights: Subint weights. (There is one value for each channel)
        """
        return self.fits['SUBINT'].data[isub]['DAT_WTS']

    def get_scales(self, isub):
        """Return scales for a particular subint.

            Inputs:
                isub: index of subint (first subint is 0)
            
            Output:
                scales: Subint scales. (There is one value for each channel)
        """
        return self.fits['SUBINT'].data[isub]['DAT_SCL']

    def get_offsets(self, isub):
        """Return offsets for a particular subint.

            Inputs:
                isub: index of subint (first subint is 0)
            
            Output:
                offsets: Subint offsets. (There is one value for each channel)
        """
        return self.fits['SUBINT'].data[isub]['DAT_OFFS']

fitsfile = PsrfitsFile('guppi_55197_GBNCC08327_0044_0001.fits')
read_subint(fitsfile,isub=0,apply_weights = False,apply_offsets = False,apply_scales=False)
