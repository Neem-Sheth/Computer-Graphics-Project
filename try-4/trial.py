from tkinter import Tk, Canvas, Button, Entry, Scale, Label, filedialog, HORIZONTAL
from PIL import Image, ImageDraw, ImageTk

# Load the image function
def load_image():
    global img, original_img
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path).convert('RGB')
        original_img = img.copy()
        display_image(img)

# Display image on the canvas
def display_image(image):
    global img_tk
    img_tk = ImageTk.PhotoImage(image)
    canvas.create_image(250, 250, image=img_tk)

# Reset the image to original
def reset_image():
    global img
    img = original_img.copy()
    display_image(img)

# Translation
def translate():
    dx = int(translate_x_entry.get())
    dy = int(translate_y_entry.get())
    global img
    width, height = img.size
    new_img = Image.new('RGB', (width, height), 'white')
    for x in range(width):
        for y in range(height):
            if 0 <= x + dx < width and 0 <= y + dy < height:
                new_img.putpixel((x + dx, y + dy), img.getpixel((x, y)))
    img = new_img
    display_image(img)

# Rotation
def rotate():
    angle = int(rotate_entry.get())
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

# Scaling
def scale():
    sx = scale_x_slider.get()
    sy = scale_y_slider.get()
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

# Reflection
def reflect():
    axis = reflect_axis_entry.get().lower()
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

# Shear
def shear():
    shear_x = shear_x_slider.get()
    shear_y = shear_y_slider.get()
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

# Clipping
def clip():
    x_min = int(clip_x_min_entry.get())
    y_min = int(clip_y_min_entry.get())
    x_max = int(clip_x_max_entry.get())
    y_max = int(clip_y_max_entry.get())
    global img
    new_img = Image.new('RGB', img.size, 'white')
    draw = ImageDraw.Draw(new_img)

    for x in range(img.width):
        for y in range(img.height):
            if x_min <= x <= x_max and y_min <= y <= y_max:
                new_img.putpixel((x, y), img.getpixel((x, y)))
            else:
                draw.point((x, y), fill='white')

    img = new_img
    display_image(img)

# Initialize GUI
root = Tk()
root.title("Interactive Image Transformations")

canvas = Canvas(root, width=500, height=500, bg='white')
canvas.grid(row=0, column=0, columnspan=6)

Button(root, text="Load Image", command=load_image).grid(row=1, column=0)
Button(root, text="Reset", command=reset_image).grid(row=1, column=1)

# Translate Controls
Label(root, text="Translate X").grid(row=2, column=0)
translate_x_entry = Entry(root)
translate_x_entry.grid(row=2, column=1)

Label(root, text="Translate Y").grid(row=2, column=2)
translate_y_entry = Entry(root)
translate_y_entry.grid(row=2, column=3)

Button(root, text="Translate", command=translate).grid(row=2, column=4)

# Rotate Controls
Label(root, text="Rotate Angle").grid(row=3, column=0)
rotate_entry = Entry(root)
rotate_entry.grid(row=3, column=1)
Button(root, text="Rotate", command=rotate).grid(row=3, column=4)

# Scale Controls
Label(root, text="Scale X").grid(row=4, column=0)
scale_x_slider = Scale(root, from_=0.1, to=3.0, orient=HORIZONTAL, resolution=0.1)
scale_x_slider.grid(row=4, column=1)

Label(root, text="Scale Y").grid(row=4, column=2)
scale_y_slider = Scale(root, from_=0.1, to=3.0, orient=HORIZONTAL, resolution=0.1)
scale_y_slider.grid(row=4, column=3)

Button(root, text="Scale", command=scale).grid(row=4, column=4)

# Reflect Controls
Label(root, text="Reflect Axis (horizontal/vertical)").grid(row=5, column=0)
reflect_axis_entry = Entry(root)
reflect_axis_entry.grid(row=5, column=1)
Button(root, text="Reflect", command=reflect).grid(row=5, column=4)

# Shear Controls
Label(root, text="Shear X").grid(row=6, column=0)
shear_x_slider = Scale(root, from_=-1.0, to=1.0, orient=HORIZONTAL, resolution=0.1)
shear_x_slider.grid(row=6, column=1)

Label(root, text="Shear Y").grid(row=6, column=2)
shear_y_slider = Scale(root, from_=-1.0, to=1.0, orient=HORIZONTAL, resolution=0.1)
shear_y_slider.grid(row=6, column=3)

Button(root, text="Shear", command=shear).grid(row=6, column=4)

# Clip Controls
Label(root, text="Clip X Min").grid(row=7, column=0)
clip_x_min_entry = Entry(root)
clip_x_min_entry.grid(row=7, column=1)

Label(root, text="Clip Y Min").grid(row=7, column=2)
clip_y_min_entry = Entry(root)
clip_y_min_entry.grid(row=7, column=3)

Label(root, text="Clip X Max").grid(row=8, column=0)
clip_x_max_entry = Entry(root)
clip_x_max_entry.grid(row=8, column=1)

Label(root, text="Clip Y Max").grid(row=8, column=2)
clip_y_max_entry = Entry(root)
clip_y_max_entry.grid(row=8, column=3)

Button(root, text="Clip", command=clip).grid(row=8, column=4)

root.mainloop()
