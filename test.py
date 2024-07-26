import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def create_image_with_text():
    # Tạo một hình ảnh đơn giản với Pillow
    image = Image.new("RGB", (400, 200), color=(73, 109, 137))
    return image


def display_image_and_entries(image, entries_data):
    root = tk.Tk()
    root.title("Image with Multiple Entries")

    # Chuyển đổi ảnh để sử dụng với tkinter
    img_tk = ImageTk.PhotoImage(image)

    # Tạo Canvas để hiển thị hình ảnh
    canvas = tk.Canvas(root, width=image.width, height=image.height)
    canvas.pack(fill="both", expand=True)

    # Vẽ hình ảnh lên Canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    # Tạo và đặt nhiều Entry trên Canvas
    for entry_data in entries_data:
        text, x, y = entry_data
        text_var = tk.StringVar()
        text_var.set(text)
        text_entry = ttk.Entry(root, textvariable=text_var, width=50)

        # Đặt Entry trên Canvas tại vị trí x, y
        canvas.create_window(x, y, anchor=tk.NW, window=text_entry)

    root.mainloop()


# Tạo hình ảnh
image = create_image_with_text()

# Dữ liệu cho các Entry: mỗi phần tử gồm (văn bản, x, y)
entries_data = [
    ("Hello World!", 10, 10),
    ("This is entry 2", 10, 50),
    ("Another entry here", 10, 90),
    ("More text", 10, 130),
]

# Hiển thị hình ảnh và các Entry
display_image_and_entries(image, entries_data)
