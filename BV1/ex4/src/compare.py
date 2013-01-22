#!/usr/bin/env python

from PIL import Image

import removenoise

def diff(img1, img2) :
	counter = 0
	for i in range(img1.size[0]) :
		for j in range(img1.size[1]) :
			if img1.getpixel((i, j)) != img2.getpixel((i, j)) :
				counter += 1
	return counter

if __name__ == '__main__' :
	img = Image.open('../data/Testbild-mit-Rauschen.png')
	img = img.convert('L')
	img1 = Image.open('../data/Testbild-ohne-Rauschen.png')
	img1 = img1.convert('L')
	img2 = removenoise.removenoise(img)
	print diff(img, img1)
	print diff(img, img2)
	print diff(img1, img2)

