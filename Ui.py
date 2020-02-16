#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter
import re
import os
import time
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from past.builtins import execfile
from Predict import *


class Notepad:

    __root = Tk()

    # default window width and height
    __width = 400
    __height = 300
    __text_area = Text(__root)
    __menu_bar = Menu(__root)
    __scale_bar = Scale(
                __menu_bar,
                from_=14,
                to=30,
                orient='horizontal'
            )

    __file_menu = Menu(__menu_bar, tearoff=0)
    __edit_menu = Menu(__menu_bar, tearoff=0)

    # title
    __title = 'Untitled - AutoS-Notepad'
    # To add scrollbar
    __scroll_bar = Scrollbar(__text_area)
    __file = None

    def __init__(self, model, **kwargs):
        # set window size
        try:
            self.__width = kwargs['width']
        except KeyError:
            pass

        try:
            self.__height = kwargs['height']
        except KeyError:
            pass

        # SET UP MODEL
        self.model = model

        # WINDOW -------------------------------

        # Set the window text
        self.__root.title(self.__title)

        # Center the window
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()

        # For left-alling
        left = screen_width/ 2 - self.__width / 2

        # For right-allign
        top = screen_height / 2 - self.__height / 2

        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d'
                % (self.__width,
                   self.__height, left, top))

        # MENU -------------------------------

        # To open new file
        self.__file_menu.add_command(
                label='New',
                command=self.newFile,
                accelerator="Ctrl+N")

        # To open a already existing file
        self.__file_menu.add_command(
                label='Open',
                command=self.openFile,
                accelerator="Ctrl+O")

        # To save current file
        self.__file_menu.add_command(
                label='Save',
                command=self.saveFile,
                accelerator="Ctrl+S")

        # To create a line in the dialog
        self.__file_menu.add_separator()

        self.__file_menu.add_command(label='Exit',
                command=self.quitApplication,
                accelerator='Ctrl+Q')

        self.__menu_bar.add_cascade(label='File',
                menu=self.__file_menu)

        # To give a feature of cut
        self.__edit_menu.add_command(
                label='Cut',
                command=self.cut)

        # to give a feature of copy
        self.__edit_menu.add_command(
                label='Copy',
                command=self.copy)

        # To give a feature of paste
        self.__edit_menu.add_command(
                label='Paste',
                command=self.paste)

        # To give a feature of editing
        self.__menu_bar.add_cascade(
                label='Edit',
                menu=self.__edit_menu)

        self.__root.config(menu=self.__menu_bar)


        # SCROLLBAR -------------------------------

        # Scrollbar will adjust automatically according to the content
        self.__scroll_bar.pack(side=RIGHT, fill=Y)
        self.__scroll_bar.config(command=self.__text_area.yview)

        # TEXTAREA -------------------------------

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__text_area.grid(sticky=N + E + S + W)
        self.__text_area.config(yscrollcommand=self.__scroll_bar.set)

        # set default font size
        self.__text_area.config(font=('Time New Roman', 25))

        # get fired when encounter
        # one of the delimiters
        __txt_area_binding_list = [
                    ("<KeyRelease>", self.call_detection),
                    ("<Control-Key-n>", self.newFile),
                    ("<Control-Key-o>", self.openFile),
                    ("<Control-Key-q>", self.quitApplication),
                    ("<Control-Key-s>", self.saveFile)
                ]

        for ctr_key, func in __txt_area_binding_list:
            self.__text_area.bind(ctr_key, func)

    ############## METHOD ####################

    # QUIT
    def quitApplication(self, event=None):
        self.__root.destroy()

    # OPENFILE
    def openFile(self, event=None):

        self.__file = askopenfilename(
                defaultextension='.txt',
                filetypes=[
                    ('All Files', '*.*'),
                    ('Text Documents','*.txt')
                    ]
                )

        if self.__file == '':
            # no file to open
            self.__file = None
        else:
            # Try to open the file
            # set the window title
            notepad_name = ' AutoS-Notepad'
            self.__root.title(
                    os.path.basename(self.__file)
                    + notepad_name)

            self.__text_area.delete(1.0, END)

            with open(self.__file, 'r') as file:
                self.__text_area.insert(1.0, file.read())

    # NEWFILE
    def newFile(self, event=None):

        self.__root.title('Untitled - AutoS-Notepad')
        self.__file = None
        self.__text_area.delete(1.0, END)

    # SAVEFILE
    def saveFile(self, event=None):

        if self.__file == None:

            # Save as new file
            self.__file = asksaveasfilename(
                    initialfile='Untitled.txt',
                    defaultextension='.txt',
                    filetypes=[
                        ('All Files','*.*'),
                        ('Text Documents', '*.txt')
                        ]
                    )

            if self.__file == '':
                self.__file = None
            else:

                # Try to save the file
                with open(self.__file, 'w') as file:
                    file.write(self.__text_area.get(1.0, END))

                # Change the window title
                self.__root.title(
                        os.path.basename(self.__file)
                        + ' - Notepad')
        else:
            with open(self.__file, 'w') as file:
                file.write(self.__text_area.get(1.0, END))

    # TEXT MANIPULATION

    def cut(self):
        self.__text_area.event_generate('<<Cut>>')

    def copy(self):
        self.__text_area.event_generate('<<Copy>>')

    def paste(self):
        self.__text_area.event_generate('<<Paste>>')

    # TEXT RESIZING
    def resize_font(self, event=None):
        self.__text_area.config(
                    font=(
                            'Time New Roman',
                            self.__scale_bar.get()
                        )
                )

    __triggers = [
        ' ', '.', '!', '?', '\n'
    ]

    # call_detection is called whenever key is released
    def call_detection(self, event):
        key_typed = event.char

        if key_typed in self.__triggers:
            typed_str = self.__text_area.get(1.0, END)

            # If space is found then move else cut
            delim_str = typed_str
            if key_typed != ' ':
                delim_str = typed_str[typed_str.rfind(key_typed)+1:]

            # MODEL PREDICTION IS HERE
            self.model.predict(delim_str)


    def run(self):
        # Run main application
        self.__root.mainloop()


# Run main application
if __name__ == '__main__':
    model = Predict("austen-emma.txt", t_size=50)
    notepad = Notepad(model)
    notepad.run()
