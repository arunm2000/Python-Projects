#Import Libs and Modules
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image

#Function to Browse for Image
def browse():
    global img
    filename = filedialog.askopenfilename(title = "Select a File")
    img = Image.open(filename)

#Function to Change from PNG to JPEG
def png_to_jpg():
    global img
    export_file_path = filedialog.asksaveasfilename(defaultextension='.jpg')
    img.save(export_file_path)

#Function to Change from JPEG to PNG
def jpg_to_png():
    global img
    export_file_path = filedialog.asksaveasfilename(defaultextension='.png')
    img.save(export_file_path)

#Create Window
root = Tk()
root.geometry('600x150')
root.title('Image Converter')

Label(root, text='Image Converter', font=('Comic Sans MS', 15)).place(x=210, y=10)

Button(root, text='Select an Image', command=browse, fg='blue', font=('Times New Roman', 13)).place(x=225, y=45)

Button(root, text='PNG to JPEG', command=png_to_jpg, fg='red', font=('Times New Roman', 13)).place(x=100, y=95)

Button(root, text='JPEG to PNG', command=jpg_to_png, fg='red', font=('Times New Roman', 13)).place(x=350, y=95)

root.mainloop()
