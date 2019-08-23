import math
import random
from PIL import Image, ImageDraw

# canvas
width = 899
height = 899
img = Image.new("RGB", (width + 1, height + 1))
draw = ImageDraw.Draw(img)

# init
cNum = random.randint(1, 7)
max_Cize = int(min(width, height) / 4)
min_Cize = 10
xCircle = []
yCircle = []
rCircle = []

# create circles
for indexCircle in range(cNum):
    # circles cannot touch
    while(True):
        circle_radius = random.randint(min_Cize, max_Cize)
        x_pos = random.randint(circle_radius, width - circle_radius)
        y_pos = random.randint(circle_radius, height - circle_radius)
        flag = True
        if indexCircle > 0:
            for j in range(indexCircle):
                if math.hypot(x_pos - xCircle[j], y_pos - yCircle[j]) < circle_radius + rCircle[j]:
                    flag = False
                    break
        if flag == True:
            break
    # draw circle when not touching
    draw.ellipse((x_pos - circle_radius, y_pos - circle_radius, x_pos + circle_radius, y_pos + circle_radius))
    xCircle.append(x_pos)
    yCircle.append(y_pos)
    rCircle.append(circle_radius)

# spawn ball in open area
flag = False
while(flag != True):
    x = float(random.randint(0, width))
    y = float(random.randint(0, height))
    # respawn until not in a circle
    for indexCircle in range(cNum):
        if math.hypot(x - xCircle[indexCircle], y - yCircle[indexCircle]) <= rCircle[indexCircle]:
            flag = True
        else :
            flag = False

draw.ellipse((x, y, x+5, y+10))
img.save("start.png", "PNG")


# ball movement
vector = 2.0 * math.pi * random.random()
vx = math.cos(vector)
vy = math.sin(vector)

for steps in range(20000):
    # add path
    img.putpixel((int(x), int(y)), (255, 0, 0))
    xnew = x + vx
    ynew = y + vy

    # walls
    if xnew < 0 or xnew > width:
        vx = -vx
        xnew = x
    if ynew < 0 or ynew > height:
        vy = -vy
        ynew = y

    # bounce off circles
    for indexCircle in range(cNum):
        if math.hypot(xnew - xCircle[indexCircle], ynew - yCircle[indexCircle]) <= rCircle[indexCircle]:
            angle_into_circle = math.atan2(ynew - yCircle[indexCircle], xnew - xCircle[indexCircle])
            reverse_angle = math.atan2(-vy, -vx)
            reflected_direction = reverse_angle + (angle_into_circle - reverse_angle) * 2
            vy = math.sin(reflected_direction)
            vx = math.cos(reflected_direction)
            xnew = x
            ynew = y

    x = xnew
    y = ynew

# final output
img.save("ballPath.png", "PNG")
