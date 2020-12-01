import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import randint
from hashlib import md5
from time import localtime
import uuid
import tempfile
import os
import image_grid

# pip install Pillow 

##### Settings #####
grid_size = 3,4 # columns x rows

workdir = '.' # default: "." - current folder
out_file = './_out.jpg'
#out_file = tempfile.mkstemp('.jpg', 'grid', '.')[1])
image_exts = ('.png')
###############################

# count cards and check lowest common resolution
cards = 0
lowest_common_resolution = 0
for f in os.listdir(workdir):
    if f.lower().endswith(image_exts) and f != out_file:
        cards += 1
        im = Image.open(f)
        w,h = im.size
        if lowest_common_resolution == 0 or w < lowest_common_resolution[0] or h < lowest_common_resolution[1]:
            lowest_common_resolution = w,h


print (cards, "cards")
print ("lowest common resolution:", lowest_common_resolution)

per_row = grid_size[0]
rows = grid_size[1]
card_resolution = lowest_common_resolution

out_width = card_resolution[0] * per_row
out_height = card_resolution[1] * rows
out_image = Image.new("RGB", (out_width, out_height))

x = 0
y = 0
for f in os.listdir(workdir):
    if f.lower().endswith(image_exts) and f != out_file:
        # load image
        #print f
        im = Image.open(os.path.join(workdir, f))
        if im.size != card_resolution:
            print ("resizing",f,"from",im.size,"to",card_resolution)
            im = im.resize((card_resolution))
        coords = (x*card_resolution[0], y*card_resolution[1])
        out_image.paste(im, coords)
        x += 1
        if x == per_row:
            x = 0
            y += 1

#print ("saving grid with resolution",out_image.size,"to",out_file)
out_image.save(tempfile.mkstemp('.jpg', 'grid', '.')[1])