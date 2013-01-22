'''
	Image Processing 1 - Exercise 2 - WiSe 2012/13

	Author : Weipeng He
	Email : 2he@informatik.uni-hamburg.de

	Description : 
		Measure the brightness value (intensity) of the given picture
'''

from PIL import Image

# measure and print the brightness of img.
def measure (img) :
	w, h = img.size
	data = img.load()
	for i in range(0, h) :
		for j in range(0, w) :
			bright = sum(data[j,i]) / 3
			print bright,
		print ''

def main() :
	img = Image.open("../data/B1.png")
	measure(img)

if __name__ == "__main__" :
	main()
