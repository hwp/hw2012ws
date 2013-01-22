#!/usr/bin/env python

from PIL import Image

R = 10

def isnoise(img, x, y) :
	pv = img.getpixel((x, y))
	greater = False
	less = False
	near = False
	for i in (x - 1, x, x + 1) :
		if i >= 0 and i < img.size[0] :
			for j in (y - 1, y, y + 1) :
				if j >= 0 and j < img.size[1] and not (i == x and j == y) :
					if img.getpixel((i, j)) > pv + R :
						greater = True
					elif img.getpixel((i, j)) < pv - R :
						less = True
					else :
						near = True
	return not (near or (less and greater))

def medianfilter(img, x, y) :
	neighbor = []
#	print '-----' + str((x, y)) + '-----'
#	for i in (x - 1, x, x + 1) :
#		for j in (y - 1, y, y + 1) :
#			if i >= 0 and i < img.size[0] and j >= 0 and j < img.size[1] :
#				print img.getpixel((i, j)),
#			else :
#				print 'x',
#		print ''
	for i in (x - 1, x, x + 1) :
		if i >= 0 and i < img.size[0] :
			for j in (y - 1, y, y + 1) :
				if j >= 0 and j < img.size[1] :
					neighbor.append(img.getpixel((i, j)))
#	print '->' + str(sorted(neighbor)[len(neighbor) / 2]);
	return sorted(neighbor)[len(neighbor) / 2]

def removenoise(img) :
	img2 = img.copy()
	(x, y) = img.size
	counter = 0
	for i in range(x) :
		for j in range(y) :
			if isnoise(img, i, j) :
				counter += 1
				img2.putpixel((i, j), medianfilter(img, i, j))
	print str(counter) + ' noise pixels found'
	return img2

if __name__ == '__main__' :
	img = Image.open('../data/Testbild-mit-Rauschen.png')
	img = img.convert('L')
	img = removenoise(img)
	img.save('../data/Testbild-remove-Rauschen.png')

