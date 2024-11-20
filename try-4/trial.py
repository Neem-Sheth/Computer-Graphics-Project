from tkinter import Tk, Canvas, Button, Entry, Scale, Label, filedialog, HORIZONTAL, Frame
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

def flood_fill():
    try:
        xmin = int(flood_fill_xmin_entry.get())
        ymin = int(flood_fill_ymin_entry.get())
        xmax = int(flood_fill_xmax_entry.get())
        ymax = int(flood_fill_ymax_entry.get())
        fill_color_input = flood_fill_color_entry.get().strip()
        
        # Remove any parentheses and whitespace
        fill_color = tuple(map(int, fill_color_input.replace('(', '').replace(')', '').split(',')))

        if len(fill_color) != 3 or any(c < 0 or c > 255 for c in fill_color):
            raise ValueError("Fill color must be three integers between 0 and 255.")

        global img
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Ensure bounds are within the image dimensions
        xmin = max(0, min(xmin, width - 1))
        ymin = max(0, min(ymin, height - 1))
        xmax = max(0, min(xmax, width - 1))
        ymax = max(0, min(ymax, height - 1))

        # Apply the color filter (blending original and fill_color)
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                original_color = img.getpixel((x, y))
                
                # Blend original color with the fill color (simple linear interpolation)
                blended_color = tuple(
                    int(original_color[i] * 0.5 + fill_color[i] * 0.5)  # 50% blend
                    for i in range(3)
                )
                
                # Set the new color (blended color)
                draw.point((x, y), fill=blended_color)

        display_image(img)  # Update the image display
    except ValueError as e:
        print(f"Error: {e}")

# Initialize GUI
root = Tk()
root.title("Interactive Image Transformations")
root.geometry('1200x600')  # Adjust window size to fit laptop screen

# Frame for Image (left side)
image_frame = Frame(root, width=600, height=600, bg='gray')
image_frame.grid(row=0, column=0, rowspan=12)

# Canvas for Image Display
canvas = Canvas(image_frame, width=500, height=500, bg='white')
canvas.grid(row=0, column=0, padx=20, pady=20)

# Controls Frame (right side)
controls_frame = Frame(root, width=600, height=600, bg='lightgray')
controls_frame.grid(row=0, column=1, rowspan=12, padx=20, pady=20)

# Load Image and Reset Buttons
Button(controls_frame, text="Load Image", command=load_image).grid(row=1, column=0, pady=5)
Button(controls_frame, text="Reset", command=reset_image).grid(row=1, column=1, pady=5)

# Translate Controls
Label(controls_frame, text="Translate X").grid(row=2, column=0)
translate_x_entry = Entry(controls_frame)
translate_x_entry.grid(row=2, column=1)

Label(controls_frame, text="Translate Y").grid(row=2, column=2)
translate_y_entry = Entry(controls_frame)
translate_y_entry.grid(row=2, column=3)

Button(controls_frame, text="Translate", command=translate).grid(row=2, column=4)

# Rotate Controls
Label(controls_frame, text="Rotate Angle").grid(row=3, column=0)
rotate_entry = Entry(controls_frame)
rotate_entry.grid(row=3, column=1)
Button(controls_frame, text="Rotate", command=rotate).grid(row=3, column=4)

# Scale Controls
Label(controls_frame, text="Scale X").grid(row=4, column=0)
scale_x_slider = Scale(controls_frame, from_=0.1, to=3.0, orient=HORIZONTAL, resolution=0.1)
scale_x_slider.grid(row=4, column=1)

Label(controls_frame, text="Scale Y").grid(row=4, column=2)
scale_y_slider = Scale(controls_frame, from_=0.1, to=3.0, orient=HORIZONTAL, resolution=0.1)
scale_y_slider.grid(row=4, column=3)

Button(controls_frame, text="Scale", command=scale).grid(row=4, column=4)

# Reflect Controls
Label(controls_frame, text="Reflect Axis (horizontal/vertical)").grid(row=5, column=0)
reflect_axis_entry = Entry(controls_frame)
reflect_axis_entry.grid(row=5, column=1)
Button(controls_frame, text="Reflect", command=reflect).grid(row=5, column=4)

# Shear Controls
Label(controls_frame, text="Shear X").grid(row=6, column=0)
shear_x_slider = Scale(controls_frame, from_=-1.0, to=1.0, orient=HORIZONTAL, resolution=0.1)
shear_x_slider.grid(row=6, column=1)

Label(controls_frame, text="Shear Y").grid(row=6, column=2)
shear_y_slider = Scale(controls_frame, from_=-1.0, to=1.0, orient=HORIZONTAL, resolution=0.1)
shear_y_slider.grid(row=6, column=3)

Button(controls_frame, text="Shear", command=shear).grid(row=6, column=4)

# Clip Controls
Label(controls_frame, text="Clip X Min").grid(row=7, column=0)
clip_x_min_entry = Entry(controls_frame)
clip_x_min_entry.grid(row=7, column=1)

Label(controls_frame, text="Clip Y Min").grid(row=7, column=2)
clip_y_min_entry = Entry(controls_frame)
clip_y_min_entry.grid(row=7, column=3)

Label(controls_frame, text="Clip X Max").grid(row=8, column=0)
clip_x_max_entry = Entry(controls_frame)
clip_x_max_entry.grid(row=8, column=1)

Label(controls_frame, text="Clip Y Max").grid(row=8, column=2)
clip_y_max_entry = Entry(controls_frame)
clip_y_max_entry.grid(row=8, column=3)

Button(controls_frame, text="Clip", command=clip).grid(row=8, column=4)

# Flood Fill Controls
Label(controls_frame, text="Flood Fill - X Min").grid(row=9, column=0)
flood_fill_xmin_entry = Entry(controls_frame)
flood_fill_xmin_entry.grid(row=9, column=1)

Label(controls_frame, text="Flood Fill - Y Min").grid(row=9, column=2)
flood_fill_ymin_entry = Entry(controls_frame)
flood_fill_ymin_entry.grid(row=9, column=3)

Label(controls_frame, text="Flood Fill - X Max").grid(row=10, column=0)
flood_fill_xmax_entry = Entry(controls_frame)
flood_fill_xmax_entry.grid(row=10, column=1)

Label(controls_frame, text="Flood Fill - Y Max").grid(row=10, column=2)
flood_fill_ymax_entry = Entry(controls_frame)
flood_fill_ymax_entry.grid(row=10, column=3)

Label(controls_frame, text="Fill Color (R,G,B)").grid(row=11, column=0)
flood_fill_color_entry = Entry(controls_frame)
flood_fill_color_entry.grid(row=11, column=1)

Button(controls_frame, text="Flood Fill", command=flood_fill).grid(row=11, column=4)

# Run the application
root.mainloop()