# for slide presenting purpose

from PIL import Image, ImageTk, ImageFile
from itertools import cycle
from os import listdir
from os.path import isfile, join
import Tkinter as tk
import os
import config
from config import *

class App(tk.Tk):
    start = None
    # set milliseconds time between slides
    delay = config.slide_delay
    # upper left corner coordinates of app window
    x = 100
    y = 50

    '''Tk window/label adjusts to size of image'''
    def __init__(self, folder):
        mypath = os.getcwd() + '/.tmp/' + folder
        only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        image_files = []
        for i in only_files:
            n = mypath + "/" + i
            image_files.append(n)
        DM('preseting dir {}'.format(folder))

        # the root will be self
        tk.Tk.__init__(self)
        # set x, y position only
        self.geometry('+{}+{}'.format(self.x, self.y))
        # allows repeat cycling through the pictures
        # store as (img_object, img_name) tuple
        self.pictures = cycle(((ImageTk.PhotoImage(Image.open(image)), image)
            for image in image_files))
        self.picture_display = tk.Label(self)
        self.picture_display.pack()
        self.show_slides()

    def show_slides(self):
        '''cycle through the images and show them'''
        # next works with Python26 or higher
        img_object, img_name = next(self.pictures)
        if self.start is None:
            self.start = img_name
        elif self.start == img_name:
            self.destroy()
            return

        self.picture_display.config(image=img_object)
        # shows the image filename, but could be expanded
        # to show an associated description of the image
        self.title(img_name)
        DM('presenting {}'.format(img_name))
        self.after(self.delay, self.show_slides)

    def run(self):
        self.mainloop()

# app = App("Y9e3DMJexlctd9pAudL-5A")
# app.run()
