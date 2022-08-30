import numpy
from PIL import Image
import numpy as np
num = 1
pic_raw = Image.open("./1-2.jpg")
pic_old = Image.open("./1-1.jpg")

raw = np.asarray(pic_raw)
old = np.asarray(pic_old)

for row in range(len(raw)):
    for col in range(len(raw[0])):
        if raw[row][col][0] == old[row][col][0] and raw[row][col][1] == old[row][col][1] and raw[row][col][2] == old[row][col][2]:
            pass
        else:
            if col<350:
                raw[row][col]=old[row][col]

image = Image.fromarray(raw)
image.save(f"./{num}.jpg")
numpy.save(f"./{num}.npy",raw)
image.show()


pic_old = Image.open("./1-2.jpg")
raw = numpy.load("1.npy")
old = np.asarray(pic_old)

# test
for row in range(len(raw)):
    for col in range(len(raw[0])):
        if raw[row][col][0] == old[row][col][0] and raw[row][col][1] == old[row][col][1] and raw[row][col][2] == old[row][col][2]:
            raw[row][col]=[255,255,255]

image = Image.fromarray(raw)
image.show()

