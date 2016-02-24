import numpy
import fitsio
from fitsio import FITS,FITSHDR

filename = 'guppi_55197_GBNCC08327_0044_0001.fits'
data = fitsio.read(filename, rows=[1,2], columns=['DATA'])
print data
