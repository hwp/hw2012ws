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
		if lx < MAX_SIZE \
			and density(integral, x - lx - MARGIN_SIZE, x - lx, y - ly, y + ry) > MARGIN_THRESHOLD \
			and x - lx - MARGIN_SIZE > 0:
			lx = lx + 1
			cont = True
		if rx < MAX_SIZE \
			and density(integral, x + rx, x + rx + MARGIN_SIZE, y - ly, y + ry) > MARGIN_THRESHOLD \
			and x + rx + MARGIN_SIZE < integral.shape[0] - 1:
			rx = rx + 1
			cont = True
		if ly < MAX_SIZE \
			and density(integral, x - lx, x + rx, y - ly - MARGIN_SIZE, y - ly) > MARGIN_THRESHOLD \
			and y - ly - MARGIN_SIZE > 0:
			ly = ly + 1
			cont = True
		if ry < MAX_SIZE \
			and density(integral, x - lx, x + rx, y + ry, y + ry + MARGIN_SIZE) > MARGIN_THRESHOLD \
			and y + ry + MARGIN_SIZE < integral.shape[1] - 1:
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
	MAX_SHIFT = 20
	image = (image * 255).astype(numpy.uint8)
	temp = (temp * 255).astype(numpy.uint8)
	result = []
	detector = cv2.FeatureDetector_create('SIFT')
	extractor = cv2.DescriptorExtractor_create('SIFT')
	matcher = cv2.DescriptorMatcher_create('BruteForce')
	tmp_kp = detector.detect(temp)
	tmp_kp, tmp_ds = extractor.compute(temp, tmp_kp)
	for x, y, w, h in cands :
		cand = image[x : x + w, y : y + h]
		img_kp = detector.detect(cand)
		img_kp, img_ds = extractor.compute(cand, img_kp)
		if img_ds is None :
			continue
		mm = matcher.match(tmp_ds, img_ds)
		dx = []
		dy = []
		dist = []
		for m in mm :
			kp1 = tmp_kp[m.queryIdx]
			kp2 = img_kp[m.trainIdx]
			dx.append(kp2.pt[1] - kp1.pt[1])
			dy.append(kp2.pt[0] - kp1.pt[0])
			dist.append(m.distance)
		score = 1.0 / (.1 + numpy.power(dist, 2))
		score = score / numpy.max(score)
		score[score < 0.4] = 0.0
		mdx =  numpy.sum(numpy.multiply(score, dx)) / numpy.sum(score)
		mdy =  numpy.sum(numpy.multiply(score, dy)) / numpy.sum(score)
		s2 = numpy.power(dx - mdx, 2) + numpy.power(dy - mdy, 2)
		quality = numpy.sqrt(numpy.sum(numpy.multiply(score, s2)) / (numpy.sum(score) - 1))
		if quality > 0 and quality < 2.0 and abs(mdx) < MAX_SHIFT and abs(mdy) < MAX_SHIFT :
			result.append((int(round(mdx)) + x, int(round(mdy)) + y))
	return result

if __name__ == '__main__' :
	image = cv2.imread(sys.argv[1], cv2.CV_LOAD_IMAGE_COLOR)
	gray = preprocess(image)
	cands = find_cand(gray)

	if len(sys.argv) <= 2 :
		cv2.imwrite('preproc.png', gray * 256)
		for (x, y, w, h) in cands :
			cv2.rectangle(image, (y, x), (y + h, x + w), (255, 0, 0))
		cv2.imwrite('cand.png', image)
	else :
		temp = cv2.imread(sys.argv[2], cv2.CV_LOAD_IMAGE_COLOR)
		gtemp = preprocess(temp)
		match = find_match(gray, temp, cands)
		(w, h) = gtemp.shape
		for (x, y) in match:
			print (y, x)
			cv2.rectangle(image, (y, x), (y + h, x + w), (255, 0, 0))
		cv2.imwrite('match.png', image)
	winname = 'Find Characters (c) Weipeng He'
	cv2.namedWindow(winname, cv2.CV_WINDOW_AUTOSIZE)
	cv2.imshow(winname, image)
	cv2.waitKey(0)

