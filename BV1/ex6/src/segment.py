#!/usr/bin/env python

from PIL import Image
import numpy

from Queue import PriorityQueue

DIR = [(0, 1), (-1, 0), (0, -1), (1, 0)]

def localmin(gms, i, j) :
	for d in range(len(DIR)) :
		x = i + DIR[d][0]
		y = j + DIR[d][1]
		if x >= 0 and x < gms.shape[0] \
				and y >= 0 and y < gms.shape[1] \
				and gms[x][y] < gms[i][j] :
			return False
	return True

def addNeighbor(img, gms, taken, i, j, q) :
	for d in range(len(DIR)) :
		x = i + DIR[d][0]
		y = j + DIR[d][1]
		if x >= 0 and x < gms.shape[0] \
				and y >= 0 and y < gms.shape[1] \
				and taken[x][y] == 0 :
			taken[x][y] = 1
			img.putpixel((y, x), img.getpixel((j, i)))
			#print (y, x), img.getpixel((j, i)), (j, i)
			#print taken
			q.put((gms[x][y], (x, y)))

def segment(img) :
	g = numpy.array(img.getdata())
	g = g.reshape(img.size)
	gx = g[:-1,1:] - g[:-1,:-1]
	gy = g[1:,:-1] - g[:-1,:-1]
	gms = gx * gx + gy * gy

	seg = Image.new('L', gms.shape)
	taken = numpy.zeros(seg.size)
	#print 'original local mininum'
	for i in range(seg.size[0]) :
		for j in range(seg.size[1]) :
			if localmin(gms, i, j) :
				taken[i][j] = 1
				seg.putpixel((j, i), img.getpixel((j, i)))
				#print (j, i), img.getpixel((j, i))
	q = PriorityQueue(-1)
	#print 'expand'
	for i in range(seg.size[0]) :
		for j in range(seg.size[1]) :
			if taken[i][j] > 0 :
				addNeighbor(seg, gms, taken, i, j, q)
	#print q.qsize()
	while not q.empty() :
		(i, j) = q.get()[1]
		addNeighbor(seg, gms, taken, i, j, q)
		#print q.qsize()
	return seg

if __name__ == '__main__' :
	img = Image.open('../data/lenna.png')
	img = segment(img)
	img.save('../data/segment-2.png')

