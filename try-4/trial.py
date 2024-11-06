from tkinter import Tk, Canvas, Button, filedialog
from PIL import Image, ImageDraw, ImageTk

def load_image():
    global img, original_img
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path).convert('RGB')
        original_img = img.copy()
        display_image(img)

def display_image(image):
    global img_tk
    img_tk = ImageTk.PhotoImage(image)
    canvas.create_image(250, 250, image=img_tk)

def reset_image():
    global img
    img = original_img.copy()
    display_image(img)

def translate(dx, dy):
    global img
    width, height = img.size
    new_img = Image.new('RGB', (width, height), 'white')
    for x in range(width):
        for y in range(height):
            if 0 <= x + dx < width and 0 <= y + dy < height:
                new_img.putpixel((x + dx, y + dy), img.getpixel((x, y)))
    img = new_img
    display_image(img)

def rotate(angle):
    import math
    global img
    width, height = img.size
    cx, cy = width // 2, height // 2
    new_img = Image.new('RGB', (width, height), 'white')
    angle = math.radians(angle)
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)

    for x in range(width):
        for y in range(height):
            nx = int((x - cx) * cos_theta - (y - cy) * sin_theta + cx)
            ny = int((x - cx) * sin_theta + (y - cy) * cos_theta + cy)
            if 0 <= nx < width and 0 <= ny < height:
                new_img.putpixel((nx, ny), img.getpixel((x, y)))
    img = new_img
    display_image(img)

def scale(sx, sy):
    global img
    width, height = img.size
    new_width = int(width * sx)
    new_height = int(height * sy)
    new_img = Image.new('RGB', (new_width, new_height), 'white')

    for x in range(new_width):
        for y in range(new_height):
            src_x = int(x / sx)
            src_y = int(y / sy)
            if src_x < width and src_y < height:
                new_img.putpixel((x, y), img.getpixel((src_x, src_y)))

    img = new_img
    display_image(img)

def reflect(axis='horizontal'):
    global img
    width, height = img.size
    new_img = Image.new('RGB', (width, height), 'white')

    if axis == 'horizontal':
        for x in range(width):
            for y in range(height):
                new_img.putpixel((width - x - 1, y), img.getpixel((x, y)))
    elif axis == 'vertical':
        for x in range(width):
            for y in range(height):
                new_img.putpixel((x, height - y - 1), img.getpixel((x, y)))

    img = new_img
    display_image(img)

def shear(shear_x=0, shear_y=0):
    global img
    width, height = img.size
    new_img = Image.new('RGB', (width, height), 'white')

    for x in range(width):
        for y in range(height):
            new_x = x + int(shear_x * y)
            new_y = y + int(shear_y * x)
            if 0 <= new_x < width and 0 <= new_y < height:
                new_img.putpixel((new_x, new_y), img.getpixel((x, y)))

    img = new_img
    display_image(img)

def clip(x_min, y_min, x_max, y_max):
    global img
    new_img = Image.new('RGB', (img.size), 'white')
    draw = ImageDraw.Draw(new_img)

    for x in range(img.width):
        for y in range(img.height):
            if x_min <= x <= x_max and y_min <= y <= y_max:
                new_img.putpixel((x, y), img.getpixel((x, y)))
            else:
                draw.point((x, y), fill='white')

    img = new_img
    display_image(img)

def flood_fill(x, y, new_color):
    global img
    original_color = img.getpixel((x, y))
    width, height = img.size
    stack = [(x, y)]

    while stack:
        x, y = stack.pop()
        if img.getpixel((x, y)) == original_color:
            img.putpixel((x, y), new_color)
            stack.extend([(nx, ny) for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                          if 0 <= nx < width and 0 <= ny < height])

    display_image(img)

# Initialize GUI
root = Tk()
root.title("Interactive Image Transformations")

canvas = Canvas(root, width=500, height=500, bg='white')
canvas.pack()

Button(root, text="Load Image", command=load_image).pack(side='left')
Button(root, text="Reset", command=reset_image).pack(side='left')
Button(root, text="Translate", command=lambda: translate(50, 30)).pack(side='left')
Button(root, text="Rotate", command=lambda: rotate(45)).pack(side='left')
Button(root, text="Scale", command=lambda: scale(1.5, 1.5)).pack(side='left')
Button(root, text="Reflect", command=lambda: reflect('horizontal')).pack(side='left')
Button(root, text="Shear", command=lambda: shear(0.2, 0)).pack(side='left')
Button(root, text="Clip", command=lambda: clip(100, 100, 400, 400)).pack(side='left')
Button(root, text="Flood Fill", command=lambda: flood_fill(250, 250, (255, 0, 0))).pack(side='left')

root.mainloop()
