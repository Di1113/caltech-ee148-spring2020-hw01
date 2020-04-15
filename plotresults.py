import os
import numpy as np
import json
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Following code is used in run_predictions.py to draw bounding boxes
# 	and save images with a bounding box
""" 
# bounding box top left and bottom right coordinates 
x0, y0, x1, y1 = ind[0], ind[1], ind[0]+box_height, ind[1]+box_width 

# draw bounding box on original image
rimg = Image.fromarray(I)
draw = ImageDraw.Draw(rimg)
draw.rectangle([x0, y0, x1, y1], fill=None, outline=(255, 0, 0))

# save image to destinated folder 
folderpath = "../data/RedLights2011_Medium/result-imgs"
imgfilename = ntpath.basename(img_path)
resfn = 'oneredlight_%s' % (file_name)
rimg.save(os.path.join(folderpath, resfn))
"""


# I manually picked the good and bad results and renamed their filenames 
# Following code is used to plot image grid for presenting in report.

# good1 = Image.open("good1.jpg")
# good2 = Image.open("good2.jpg")
# good3 = Image.open("good3.jpg")
# good4 = Image.open("good4.jpg")
# good5 = Image.open("good5.jpg")
# good6 = Image.open("good6.jpg")
# f, ax = plt.subplots(2,3)
# ax[0,0].imshow(good1)
# ax[0,1].imshow(good2)
# ax[0,2].imshow(good3)
# ax[1,0].imshow(good4)
# ax[1,1].imshow(good5)
# ax[1,2].imshow(good6)
# plt.show()

bad1 = Image.open("bad1.jpg")
bad2 = Image.open("bad2.jpg")
bad3 = Image.open("bad3.jpg")
bad4 = Image.open("bad4.jpg")
bad5 = Image.open("bad5.jpg")
bad6 = Image.open("bad6.jpg")
f, ax = plt.subplots(2,3)
ax[0,0].imshow(bad1)
ax[0,1].imshow(bad3)
ax[0,2].imshow(bad2)
ax[1,0].imshow(bad4)
ax[1,1].imshow(bad5)
ax[1,2].imshow(bad6)
plt.show()