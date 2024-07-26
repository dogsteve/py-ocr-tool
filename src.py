import io
import logging
import math
import tkinter as tk
from tkinter import ttk

import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageDraw, ImageFont, ImageGrab
from pyzbar import pyzbar

logging.getLogger().setLevel(logging.ERROR)

def np_array_to_bytes(np_array):
    image = Image.fromarray(np_array.astype("uint8"))

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    img_bytes = buffer.getvalue()
    return (img_bytes, image.width, image.height)


def copy_text(event, text):
    event.widget.clipboard_clear()
    event.widget.clipboard_append(text)
    print(f"Copied to clipboard: {text}")


clipboard_data = ImageGrab.grabclipboard()
if not clipboard_data:
    raise Exception("cannot find image in clipboard")

ocr = PaddleOCR(use_angle_cls=True, lang="en")
image_np = np.array(clipboard_data)

ocr_result = ocr.ocr(image_np, cls=True)

texts = [elements[1][0] for line in ocr_result for elements in line]
boxes = [elements[0] for line in ocr_result for elements in line]
scores = [elements[1][1] for line in ocr_result for elements in line]

# max_value = max(scores)
# max_index = scores.index(max_value)

qr_data = pyzbar.decode(image_np)

root = tk.Tk()
root.title("SteveDog ScreenShot")

# Display text
np_image_data = np_array_to_bytes(image_np)
image_bytes = np_image_data[0]
i_with = np_image_data[1]
i_height = np_image_data[2]
img = tk.PhotoImage(data=image_bytes)

# Canvas
canvas = tk.Canvas(root, width=i_with, height=i_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor=tk.NW, image=img)

# Display copyable texts
for i, content in enumerate(texts):
    rec_start = boxes[i][0]
    label = tk.Label(root, text=content, font=("Arial", 12, "normal"))
    label.bind("<Button-1>", lambda event, t=content: copy_text(event, t))
    canvas.create_window(
        math.floor(rec_start[0]),
        math.floor(rec_start[1]),
        anchor=tk.NW,
        window=label,
    )


for qr in qr_data:
    rec = qr.polygon[0]
    qr_line = qr.data.decode("utf-8")
    label = tk.Label(root, text=qr_line, font=("Arial", 12, "normal"))
    label.bind("<Button-1>", lambda event, t=qr_line: copy_text(event, t))
    canvas.create_window(
        rec.x,
        rec.y,
        anchor=tk.NW,
        window=label,
    )

root.mainloop()
