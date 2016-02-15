import numpy as np
import ctypes

n = 5  
a = np.arange(n, dtype = np.double)
b = np.zeros(n, dtype = np.double)
test = ctypes.cdll.LoadLibrary("./test.so")
aptr = a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
bptr = b.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
test.test(aptr, bptr, n)

print b
