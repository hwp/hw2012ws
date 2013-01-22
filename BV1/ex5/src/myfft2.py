#!/usr/bin/env python

import numpy

SIZE = 512

def myfft(data) :
	data = data.copy()
	m, n = data.shape
	# apply fft along rows
	for i in range(m) :
		data[i:i+1,:] = numpy.fft.fft(data[i:i+1,:])
	# apply fft along columns
	for i in range(n) :
		data[:,i:i+1] = numpy.transpose(numpy.fft.fft(numpy.transpose(data[:,i:i+1])))
	return data

if __name__ == '__main__' :
	data = numpy.random.randint(0, 1000, (SIZE, SIZE)).astype(numpy.complex)
	mydata = myfft(data)
	# compare with standard output
	stddata = numpy.fft.fft2(data)
	print (numpy.abs(mydata  - stddata) < 0.000001).all()
	# using standard inverse transfrom, compare to original
	myidata = numpy.fft.ifft2(mydata)
	print (numpy.abs(myidata  - data) < 0.000001).all()

