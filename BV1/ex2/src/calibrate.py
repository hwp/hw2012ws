'''
	Image Processing 1 - Exercise 2 - WiSe 2012/13

	Author : Weipeng He
	Email : 2he@informatik.uni-hamburg.de

	Description :
		Convert a image to equally bright in every pixel.
'''

from PIL import Image, ImageOps

# set the calibrated image intensity to 80,
# which guarantees that every part of calibrated rgb values
# won't exceed 255. (3 * 80 = 240 < 255)
INTENSITY = 80.0

# Convert a image to equally bright in every pixel.
def calibrate (img) :
	img = img.copy()
	w, h = img.size
	for i in range(0, h) :
		for j in range(0, w) :
			# for every pixel
			color = img.getpixel((j, i))
			ratio = sum(color) / 3.0 / INTENSITY
			color = int(round(color[0] / ratio)), int(round(color[1] / ratio)), int(round(color[2] / ratio))
			img.putpixel((j, i), color)
	return img

def main() :
	img = Image.open("../data/B1.png")
	img = calibrate(img)
	img.show()
	img.save("../data/B2.png")
	img = ImageOps.grayscale(img)
	img.save("../data/B2-grayscale.png")

if __name__ == "__main__" :
	main()
