#!/usr/bin/env python

from PIL import Image

SIZE = 512

def genpic(begin, step) :
	img = Image.new('L', (SIZE, SIZE))
	for i in range(SIZE) :
		for j in range(SIZE) :
			img.putpixel((SIZE - 1 - i, j), begin + i / (SIZE / 4) * step)
	return img

if __name__ == '__main__' :
	img = genpic(50, 50)
	img.save('../data/pic1.png')

	img = genpic(20, 20)
	img.save('../data/pic2.png')

