from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
import requests
import io


class GetImageFromUrl(Thread):
    def __init__(self, url, obj):
        super().__init__()
        self.url = url
        self.obj = obj

    def run(self):
        try:
            request = requests.get(self.url)
            img = io.BytesIO(request.content)

            self.obj.img = {"img": img, "filename": self.url.split("/")[-1]}
            img = Image.open(img)
            img = ImageTk.PhotoImage(img)
            self.obj.config(image=img)
            self.obj.image = img

        except Exception as error:
            print(error)


def download_image(filename, img):
    if filename is None or filename == "":
        filename = img["filename"]

    with open(filename, "wb") as image:
        image.write(img["img"].getbuffer())


class AsyncImage(Label):
    def __init__(self, placeholder="", url=None, default=None):
        super().__init__()
        self.img = ""
        self.config(text=placeholder)
        if url is not None:
            self.get_img = GetImageFromUrl(url, self)
            self.get_img.start()
        else:
            self.config(text="No image to read")
        if default is not None:
            img = ImageTk.PhotoImage(Image.open(default))
            self.config(image=img)
            self.image = img

    def download_image(self):
        print(self.img)
        download_image(filename="", img=self.img)


"""
======================EXAMPLE======================

from tkinter import Tk
from tk_async_image import AsyncImage

class Master(Tk):
    url = "https://lh3.googleusercontent.com/ogw/ADGmqu_eT6821bkx5rzl6x_9VKWwFT9nufwe_JqzMCs4TA=s32-c-mo"

    def __init__(self):
        super().__init__()
        self.btn = Button(text="Download image", command=self.download)
        self.btn.pack()

        self.img = AsyncImages(placeholder="Loading image", url=self.url)
        self.img.pack()
        self.img2 = AsyncImages(placeholder="Loading Image")
        self.img2.pack()
        self.mainloop()

    def download(self):
        self.img.download_image()
"""
