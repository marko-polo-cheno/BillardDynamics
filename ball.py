import math
import random
from PIL import Image, ImageDraw

# Canvas
width = 1000
height = 1000
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# Init
x_pos_store = []
y_pos_store = []
radius_store = []
amtCircles = random.randint(3, 8)
minRadius = 10
maxRadius = int(min(width - 1, height - 1) / 3.5)


# Create circle obstacles
for i in range(amtCircles):
    
    # Circles cannot touch
    while(True):
        
        circle_radius = random.randint(minRadius, maxRadius)
        circle_x = random.randint(circle_radius, width - 1 - circle_radius)
        circle_y = random.randint(circle_radius, height - 1 - circle_radius)
        flag = True

        # See if circles are touching
        if i > 0:
            for j in range(i):
                if math.hypot(circle_x - x_pos_store[j], circle_y - y_pos_store[j]) < circle_radius + radius_store[j]:
                    flag = False
                    break
        
        if flag == True:
            break

    # Add to canvas and store
    draw.ellipse((circle_x - circle_radius, circle_y - circle_radius, circle_x + circle_radius, circle_y + circle_radius))
    x_pos_store.append(circle_x)
    y_pos_store.append(circle_y)
    radius_store.append(circle_radius)

# Spawn ball until in open
while(True):
    x = float(random.randint(0, width - 1))
    y = float(random.randint(0, height - 1))
    
    flag = False

    # Check if inside an obstacle
    for i in range(amtCircles):
        if math.hypot(x - x_pos_store[i], y - y_pos_store[i]) <= radius_store[i]:
            flag = True
            break
    
    if flag == False:
        break

# Draw spawn point
for i in range(16):
    q=i/2
    draw.ellipse((x-q,y-q,x+q,y+q))

# Move ball
vector = 2.0 * math.pi * random.random()
vy = math.sin(vector)
vx = math.cos(vector)

# Distance to travel
for i in range(10000):
    
    # Draw path followed pixel by pixel
    image.putpixel((int(x), int(y)), (255, 255, 255))

    # Update to next pixel path
    xnew = x + vx
    ynew = y + vy

    # Wall bounce
    if xnew < 0 or xnew > width - 1:
        vx = -vx
        xnew = x
    if ynew < 0 or ynew > height - 1:
        vy = -vy
        ynew = y

    # Check if the ball is in contact with an obstacle
    for i in range(amtCircles):
        if math.hypot(xnew - x_pos_store[i], ynew - y_pos_store[i]) <= radius_store[i]:

            # Find bounce angle
            angle_into_circle = math.atan2(ynew - y_pos_store[i], xnew - x_pos_store[i])
            reverse_angle = math.atan2(-vy, -vx)
            angle_reflected = reverse_angle + (angle_into_circle - reverse_angle) * 2

            # New vector
            vy = math.sin(angle_reflected)
            vx = math.cos(angle_reflected)

            # Change dymanic
            xnew = x
            ynew = y

    # Update
    x = xnew
    y = ynew

# Draw end point
draw.ellipse((x-6,y-6,x+6,y+6))

# Save to folder
image.save("ballPath.png", "PNG")
