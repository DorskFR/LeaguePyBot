import numpy
from scipy import signal

data_length = 8192

a = numpy.random.randn(data_length)
b = numpy.zeros(data_length * 2)

b[data_length/2:data_length/2+data_length] = a # This works for data_length being even

# Do an array flipped convolution, which is a correlation.
c = signal.fftconvolve(b, a[::-1], mode='valid') 

# Use numpy.correlate for comparison
d = numpy.correlate(a, a, mode='same')

# c will be exactly the same as d, except for the last sample (which 
# completes the symmetry)
numpy.allclose(c[:-1], d) # Should be True
