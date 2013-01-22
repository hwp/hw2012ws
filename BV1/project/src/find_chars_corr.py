#!/bin/env python

import sys
import numpy
from scipy.ndimage.filters import maximum_filter

sys.path.append('../lib')
import cv2

def preprocess(image) :
	GRAY_THRESHOLD = 0.68
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = 1.0 - gray.astype(numpy.float32) / numpy.max(gray) 
	gray[gray >= GRAY_THRESHOLD] = 1.0
	gray[gray < GRAY_THRESHOLD] = 0.0
	#cv2.medianBlur(gray, 3, gray)
	return gray

def charKernel() :
	R1 = 20
	R2 = 25
	MAX = 20
	MIN = -2
	size = R2 * 2 + 1
	kernel = numpy.empty((size, size));
	for i in range(size) :
		for j in range(size) :
			d = max(abs(i - R2), abs(j - R2))
			v = R1 - d
			if v > MAX :
				v = MAX
			elif v < MIN :
				v = MIN
			kernel[i, j] = v
	kernel = kernel / numpy.sum(kernel)
	return kernel

def localmax_loc(matrix) :
	maxima = (matrix == maximum_filter(matrix, 30))
	mm = numpy.max(matrix)
	THRESHOLD_MAXIMA = 0.3
	result = []
	for i in range(maxima.shape[0]) :
		for j in range(maxima.shape[1]) :
			if maxima[i, j] and matrix[i, j] > THRESHOLD_MAXIMA * mm :
				result.append((i, j))
	return result

def density(integral, x1, x2, y1, y2) :
	if x1 < 0 :
		x1 = 0
	elif x1 >= integral.shape[0] :
		x1 = integral.shape[0] - 1
	if x2 < 0 :
		x2 = 0
	elif x2 >= integral.shape[0] :
		x2 = integral.shape[0] - 1
	if y1 < 0 :
		y1 = 0
	elif y1 >= integral.shape[1] :
		y1 = integral.shape[1] - 1
	if y2 < 0 :
		y2 = 0
	elif y2 >= integral.shape[1] :
		y2 = integral.shape[1] - 1
	return (integral[x2, y2] + integral[x1, y1] - integral[x1, y2] - integral[x2, y1]) / ((x2 - x1) * (y2 - y1) * 1.0)

def local_find(integral, (x, y)) :
	INIT_SIZE = 12 
	MAX_SIZE = 30
	MARGIN_SIZE = 3
	MARGIN_THRESHOLD = .05
	lx = INIT_SIZE
	rx = INIT_SIZE
	ly = INIT_SIZE
	ry = INIT_SIZE
	cont = True
	while cont :
		cont = False
		if lx < MAX_SIZE and density(integral, x - lx - MARGIN_SIZE, x - lx, y - ly, y + ry) > MARGIN_THRESHOLD :
			lx = lx + 1
			cont = True
		if rx < MAX_SIZE and density(integral, x + rx, x + rx + MARGIN_SIZE, y - ly, y + ry) > MARGIN_THRESHOLD :
			rx = rx + 1
			cont = True
		if ly < MAX_SIZE and density(integral, x - lx, x + rx, y - ly - MARGIN_SIZE, y - ly) > MARGIN_THRESHOLD :
			ly = ly + 1
			cont = True
		if ry < MAX_SIZE and density(integral, x - lx, x + rx, y + ry, y + ry + MARGIN_SIZE) > MARGIN_THRESHOLD :
			ry = ry + 1
			cont = True
	return (x - lx - MARGIN_SIZE, y - ly - MARGIN_SIZE, lx + rx + 2 * MARGIN_SIZE, ly + ry + 2 * MARGIN_SIZE) 

def find_cand(gray) :
	kernel = charKernel()
	filtered = numpy.empty_like(gray)
	cv2.filter2D(gray, -1, kernel, filtered, (-1, -1), 0, cv2.BORDER_CONSTANT)
	ss = cv2.integral(gray)
	result = []
	cset = set()
	for loc in localmax_loc(filtered) :
		r = local_find(ss, loc)
		if r not in cset :
			result.append(r)
			cset.add(r)
	return result

def find_match(image, temp, cands) :
	result = []
	st = cv2.integral(temp)[-1, -1]
	for x, y, w, h in cands :
		cand = image[x : x + w, y : y + h]
		sc = cv2.integral(cand)[-1, -1]
		match = numpy.empty_like(cand)
		cv2.filter2D(cand, -1, temp, match, (-1, -1), 0, cv2.BORDER_CONSTANT)
		maximum = numpy.max(match)
		quality = maximum / numpy.sqrt(sc * st)
		if quality > .60 :
			for ddx in range(w) :
				for ddy in range(h) :
					if abs(match[ddx, ddy] - maximum) < 0.1 :
						dx = ddx
						dy = ddy
						break;
			result.append((dx + x - temp.shape[0] / 2, dy + y - temp.shape[1] / 2))
	return result

if __name__ == '__main__' :
	image = cv2.imread(sys.argv[1], cv2.CV_LOAD_IMAGE_COLOR)
	gray = preprocess(image)
	cands = find_cand(gray)

	if len(sys.argv) <= 2 :
		for (x, y, w, h) in cands :
			cv2.rectangle(image, (y, x), (y + h, x + w), (255, 0, 0))
		cv2.imwrite('cand.png', image)
	else :
		temp = cv2.imread(sys.argv[2], cv2.CV_LOAD_IMAGE_COLOR)
		gtemp = preprocess(temp)
		match = find_match(gray, gtemp, cands)
		(w, h) = gtemp.shape
		for (x, y) in match:
			print (y, x)
			cv2.rectangle(image, (y, x), (y + h, x + w), (255, 0, 0))
		cv2.imwrite('match.png', image)
	winname = 'Find Characters (c) Weipeng He'
	cv2.namedWindow(winname, cv2.CV_WINDOW_AUTOSIZE)
	cv2.imshow(winname, image)
	cv2.waitKey(0)

