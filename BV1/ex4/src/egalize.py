#!/usr/bin/env python

from genpic import genpic

def egalize(img) :
	hist = img.histogram()	# Original histogram
	ss = sum(hist)			# Number of pixels 
	cs = 0.0				# counter (as float)
	gmap = list()			# grayscale value map 0.0 to 1.0
	gmax = 0.0				# max grayscale value
	for i in range(len(hist)) :
		gmap.append(cs / ss)
		if hist[i] > 0 :
			gmax = cs / ss
		cs += hist[i]
	scale = (len(gmap) - 1) / gmax
		# extend max grayscale to 255 (max possible value)
	for i in range(len(gmap)) :
		gmap[i] = int(round(gmap[i] * scale))
	for i in range(img.size[0]) :
		for j in range(img.size[1]) :
			img.putpixel((i, j), gmap[img.getpixel((i, j))])

if __name__ == '__main__' :
	img = genpic(50, 50)
	egalize(img)
	img.save('../data/pic1_egal.png')

	img = genpic(20, 20)
	egalize(img)
	img.save('../data/pic2_egal.png')

