'''
This Python script generates a grid of images by taking a collection of images in a folder, resizing them to the lowest common resolution, and pasting them onto a new image in a grid layout. 
The resulting image is then saved to a file.
The script imports the necessary modules for image processing, random number generation, file handling, and creating temporary files. 
It also includes settings that can be modified to adjust the grid size, output file name, and image file extensions to be included.
The script starts by counting the number of images in the folder that match the specified file extension and determining the lowest common resolution among them. 
Then it creates a new blank image with the dimensions calculated from the grid size and the lowest common resolution of the images. 
It then loads each image from the folder, resizes it if necessary, and pastes it onto the new image at the appropriate location. 
Finally, the resulting image is saved to an image file.
'''


import textwrap  # Importing textwrap module for wrapping text
from PIL import Image, ImageDraw, ImageFont, ImageFilter  # Importing PIL modules for image processing
from random import randint  # Importing randint function from random module for generating random integers
from hashlib import md5  # Importing md5 function from hashlib module for generating MD5 hash values
from time import localtime  # Importing localtime function from time module for getting local time
import uuid  # Importing uuid module for generating UUID values
import tempfile  # Importing tempfile module for creating temporary files
import os  # Importing os module for file handling
import image_grid  # Importing image_grid module (not provided)

# pip install Pillow 

##### Settings #####
grid_size = 3,4  # Setting the number of columns and rows in the grid
workdir = '.'  # Setting the working directory to the current folder
out_file = './_out.jpg'  # Setting the output file name and location
#out_file = tempfile.mkstemp('.jpg', 'grid', '.')[1])  # Alternative output file location (creates a temporary file)
image_exts = ('.png')  # Setting the file extensions of the images to be included in the grid
###############################

# Counting cards and checking the lowest common resolution
cards = 0
lowest_common_resolution = 0
for f in os.listdir(workdir):  # Iterating through files in the working directory
    if f.lower().endswith(image_exts) and f != out_file:  # Checking if the file has the correct extension and is not the output file
        cards += 1  # Incrementing the number of cards
        im = Image.open(f)  # Opening the image file
        w,h = im.size  # Getting the width and height of the image
        if lowest_common_resolution == 0 or w < lowest_common_resolution[0] or h < lowest_common_resolution[1]:  # Updating the lowest common resolution
            lowest_common_resolution = w,h

# Printing the number of cards and lowest common resolution
print (cards, "cards")
print ("lowest common resolution:", lowest_common_resolution)

per_row = grid_size[0]  # Setting the number of cards per row
rows = grid_size[1]  # Setting the number of rows
card_resolution = lowest_common_resolution  # Setting the card resolution to the lowest common resolution

out_width = card_resolution[0] * per_row  # Calculating the width of the output image
out_height = card_resolution[1] * rows  # Calculating the height of the output image
out_image = Image.new("RGB", (out_width, out_height))  # Creating a new blank image with the calculated dimensions

x = 0
y = 0
for f in os.listdir(workdir):  # Iterating through files in the working directory
    if f.lower().endswith(image_exts) and f != out_file:  # Checking if the file has the correct extension and is not the output file
        # Load image
        im = Image.open(os.path.join(workdir, f))  # Opening the image file
        if im.size != card_resolution:  # Resizing the image if necessary
            print ("resizing",f,"from",im.size,"to",card_resolution)
            im = im.resize((card_resolution))  # Resizing the image
        coords = (x*card_resolution[0], y*card_resolution[1])  # Calculating the coordinates to paste the image onto the output image
        out_image.paste(im, coords)
        x += 1  # Moving to the next column
        if x == per_row:  # Checking if the maximum number of columns per row has been reached
            x = 0  # Resetting the column counter to 0
            y += 1  # Moving to the next row

#print ("saving grid with resolution",out_image.size,"to",out_file)
out_image.save(tempfile.mkstemp('.jpg', 'grid', '.')[1])  # Saving the output image to a file (either the specified file or a temporary file)
