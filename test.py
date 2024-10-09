from sense_hat import SenseHat

sense = SenseHat()

sense.clear()

r = (255, 0, 0)
g = (0, 255, 0)
b = (0, 0, 255)
O = (0, 0, 0)
X = (255, 255, 255)
Y = (100, 100, 100)


def makeX():
	x_mark = []
	for i in range(0, 8):
		for j in range(8, 0, -1):
			if i + j == 8 or i == j-1:
				x_mark.append(r)
			else:
				x_mark.append(O)
	return x_mark
	
def makeO():

	o_mark = []
	for i in range(0, 8):
		for j in range(8, 0, -1):
			if i in [2, 3, 4, 5] and j in [1, 8]:
				o_mark.append(g)
			elif i in [1, 6] and j in [2, 7]:
				o_mark.append(g)
			elif i in [0, 7] and j in range(3, 7):
				o_mark.append(g)
			else:
				o_mark.append(O)
	return o_mark
	
sense.set_pixels(makeO())
while True:
	sense.show_message('MAHIRA')
	
sense.clear()



