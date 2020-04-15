#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 03:38:14 2020

@author: godf
"""

import numpy as np
import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog

#Set up GUI
window = Tk()  #Makes main window
window.wm_title("Digital Microscope")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)
def show_frame():
    global lmain
    panelA.grid_forget()
    panelB.grid_forget()
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.image = imgtk
    lmain.configure(image=imgtk)
    lmain.after(100, show_frame) 

def select_image():
#    global root
#    root=Tk()
    global panelA, panelB
    path = filedialog.askopenfilename()
    if len(path) > 0:
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
		# OpenCV represents images in BGR order; however PIL represents
		# images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# convert the images to PIL format...
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
		# ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)
        edged = ImageTk.PhotoImage(edged)
        lmain=None
		# if the panels are None, initialize them
        if panelA is None or panelB is None:
			# the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.grid(row = 0, column=0)#, padx=10, pady=2)
			# while the second panel will store the edge map
            panelB = Label(image=edged)
            panelB.image = edged
            panelB.grid(row = 0, column=100)#, padx=10, pady=2)
		# otherwise, update the image panels
        else:
			# update the pannels
            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image = image
            panelB.image = edged
        
#Slider window (slider controls stage position)
sliderFrame = Frame(window, width=600, height=100)
sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

btn = Button(sliderFrame, text="Select an image", command=select_image)
btn.grid(row = 0, column=0, padx=10, pady=2)

btnv = Button(sliderFrame, text="Select a video", command=show_frame)
btnv.grid(row = 10, column=0, padx=10, pady=2)


panelA = None
panelB = None
window.mainloop()  #Starts GUI
#root.mainloop()
