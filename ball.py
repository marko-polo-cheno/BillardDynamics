import math
import random
from PIL import Image, ImageDraw

# Make image
img_width = 799
img_height = 599
image = ImageDraw.Draw(Image.new("RGB", (img_width + 1, img_height + 1)))

# Length of line
distance = 20000

# Obstacles setup
num_of_circles = random.randint(1, 5)
max_radius = int(min(img_width, img_height) / 4)
min_radius = 10 

# Create obstacles
x_of_circles = []
y_of_circles = []
radius_of_circles = []

# Place obstacles
for cIndex in range(num_of_circles):

    # Keep placing
    while(True):
        circle_radius = random.randint(min_radius, max_radius)
        circle_center_x = random.randint(circle_radius, img_width - circle_radius)
        circle_center_y = random.randint(circle_radius, img_height - circle_radius)

        flag = True
        
        if cIndex > 0:
            for everyCircle in range(cIndex):
                if math.hypot(circle_center_x - x_of_circles[everyCircle], circle_center_y - y_of_circles[everyCircle]) < circle_radius + radius_of_circles[everyCircle]:
                    flag = False
                    break
        if flag: #==True
            break

    # Add that obstacle
    image.ellipse((circle_center_x - circle_radius, circle_center_y - circle_radius, circle_center_x + circle_radius, circle_center_y + circle_radius))
    x_of_circles.append(circle_center_x)
    y_of_circles.append(circle_center_y)
    radius_of_circles.append(circle_radius)

# Spawn ball in open space
while(True):
    x = float(random.randint(0, img_width))
    y = float(random.randint(0, img_height))
    flag = False
    for cIndex in range(num_of_circles):
        if math.hypot(x - x_of_circles[cIndex], y - y_of_circles[cIndex]) <= radius_of_circles[cIndex]:
            flag = True
            break
    if flag == False:
        break
    
# Ball velocity
vy = math.sin(math.pi * random.random() * 2)
vx = math.cos(math.pi * random.random() * 2)

pixdata = image.Image.load()##############################

for i in range(distance):
    pixdata[x, y] == (255, 255, 255)######################
    xnew = x + vx
    ynew = y + vy

    # reflection from the walls
    if xnew < 0 or xnew > img_width:
        vx = -vx
        xnew = x
    if ynew < 0 or ynew > img_height:
        vy = -vy
        ynew = y

    # Bounce of circle
    for i in range(num_of_circles):
        if math.hypot(xnew - x_of_circles[i], ynew - y_of_circles[i]) <= radius_of_circles[i]:

            # Angle change
            v1 = math.atan2(ynew - y_of_circles[i], xnew - x_of_circles[i])
            v2 = math.atan2(-vy, -vx)
            vf = (v1 - v2) * 2 + v2


            vy = math.sin(vf)
            vx = math.cos(vf)
            xnew = x
            ynew = y

    x = xnew
    y = ynew

import sys
import urllib.request
try:
    # Add to folder
    f = open('img.png','wb')
    f.write(pixdata)
    f.close()
        
except Exception:
        print("No image")





