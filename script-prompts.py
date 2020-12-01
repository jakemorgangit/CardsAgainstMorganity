# import required classes
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import randint
from hashlib import md5
from time import localtime
import uuid
import tempfile
import os




#create image object from the input image path
try:
    image = Image.open('./background-black.png')
 
    
except IOError as e:
    print(e)



# Resize the image 
width = 388
img_w = image.size[0]
img_h = image.size[1]
wpercent = (width/float(img_w))
hsize = int((float(img_h)*float(wpercent)))
rmg = image.resize((width,hsize), Image.ANTIALIAS)
rmg.size


# Set x boundry
# Take 8% to the left for min and 50% to the left for max
x_min = (rmg.size[0] * 8) // 100
x_max = (rmg.size[0] * 50) // 100
print(x_min, x_max)



# Generate the random positioning
ran_x = randint(x_min, x_max)
print(ran_x)



# Create font object with the font file and specify desired size
# Font style is `arial` and font size is 20
font_path = 'Fonts/Roboto-Medium.ttf'
font = ImageFont.truetype(font=font_path, size=35)

def text_wrap(text, font, max_width):
    lines = []
    
    # If the text width is smaller than the image width, then no need to split
    # just add it to the line list and return
    if font.getsize(text)[0]  <= max_width:
        lines.append(text)
    else:
        #split the line by spaces to get words
        words = text.split(' ')
        i = 0
        # append every word to a line while its width is shorter than the image width
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i]+ " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines
            
        

def draw_text(text):    
    # open the background file
    img = Image.open('./background-black.png')
    
    # size() returns a tuple of (width, height) 
    image_size = img.size 
 
    # create the ImageFont instance
    font_file_path = 'Fonts/Roboto-Medium.ttf'
    font = ImageFont.truetype(font_file_path, size=30, encoding="unic")
 
    # get shorter lines
    lines = text_wrap(text, font, image_size[0])
    print(lines) # ['This could be a single line text ', 'but its too long to fit in one. ']
 


#draw_text("This could be a single line text but its too long to fit in one.")

#['This could be a ', 'single line text but ', 'its too long to fit in ', 'one. ']

# Caption


fileObj = open("./prompts.txt", "r", encoding='utf-8')
for line in fileObj.readlines():
	print(line)	
	text =(line)




#text = "A man in yoga pants with a ponytail and feather earings."
	lines = text_wrap(text, font, rmg.size[0]-ran_x)
	line_height = font.getsize('hg')[1]


	y_min = (rmg.size[1] * 4) // 100   # 4% from the top
	y_max = (rmg.size[1] * 50) //100   # 90% to the bottom
	y_max -= (len(lines)*line_height)  # Adjust base on lines and height
	#ran_y = randint(y_min, y_max)      # Generate random point

	rmg = rmg.filter(ImageFilter.SMOOTH_MORE)


	#Create draw object
	draw = ImageDraw.Draw(rmg)

	color = 'rgb(255,255,255)'  # Main text color
	x = 20
	y = 20

	for line in lines:
		draw.text((x,y), line, fill=color, font=font)
		
		y = y + line_height

	fontmorgan = ImageFont.truetype('Fonts/Roboto-Medium.ttf', size=15)
	# Footer
	(x, y) = (20, 500)
	name = 'Cards Against Morganity'
	color = 'rgb(169,169,169)' # Grey color
	draw.text((x, y), name, fill=color, font=fontmorgan)
	
	# Launch object in image viewer
	#rmg.show()
	
	
	# Save captioned image

	
	rmg.save(tempfile.mkstemp('.png', 'prompt', './prompts')[1])
	image = image.convert('RGB')
	rmg = image
	fileObj.close()

