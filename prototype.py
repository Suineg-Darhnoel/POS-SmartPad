#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter
import re
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from past.builtins import execfile
from Predict import *


class Notepad:

    __root = Tk()

    # default window width and height
    __this_width = 400
    __this_height = 300
    __this_text_area = Text(__root)
    __this_menu_bar = Menu(__root)
    __this_file_menu = Menu(__this_menu_bar, tearoff=0)
    __this_edit_menu = Menu(__this_menu_bar, tearoff=0)

    # title
    __title = 'Untitled - AutoS-Notepad'
    # To add scrollbar
    __this_scroll_bar = Scrollbar(__this_text_area)
    __file = None

    def __init__(self, **kwargs):
        # set window size
        try:
            self.__this_width = kwargs['width']
        except KeyError:
            pass

        try:
            self.__this_height = kwargs['height']
        except KeyError:
            pass

        # WINDOW -------------------------------

        # Set the window text
        self.__root.title(self.__title)

        # Center the window
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()

        # For left-alling
        left = screen_width/ 2 - self.__this_width / 2

        # For right-allign
        top = screen_height / 2 - self.__this_height / 2

        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d'
                % (self.__this_width,
                   self.__this_height, left, top))

        # MENU -------------------------------

        # To open new file
        self.__this_file_menu.add_command(
                label='New',
                command=self.newFile,
                accelerator="Ctrl+N")

        # To open a already existing file
        self.__this_file_menu.add_command(
                label='Open',
                command=self.openFile,
                accelerator="Ctrl+O")

        # To save current file
        self.__this_file_menu.add_command(
                label='Save',
                command=self.saveFile,
                accelerator="Ctrl+S")

        # To create a line in the dialog
        self.__this_file_menu.add_separator()

        self.__this_file_menu.add_command(label='Exit',
                command=self.quitApplication,
                accelerator='Ctrl+Q')

        self.__this_menu_bar.add_cascade(label='File',
                menu=self.__this_file_menu)

        # To give a feature of cut
        self.__this_edit_menu.add_command(
                label='Cut',
                command=self.cut)

        # to give a feature of copy
        self.__this_edit_menu.add_command(
                label='Copy',
                command=self.copy)

        # To give a feature of paste
        self.__this_edit_menu.add_command(
                label='Paste',
                command=self.paste)

        # To give a feature of editing
        self.__this_menu_bar.add_cascade(
                label='Edit',
                menu=self.__this_edit_menu)

        self.__root.config(menu=self.__this_menu_bar)

        # SCROLLBAR -------------------------------

        # Scrollbar will adjust automatically according to the content
        self.__this_scroll_bar.pack(side=RIGHT, fill=Y)
        self.__this_scroll_bar.config(command=self.__this_text_area.yview)

        # TEXTAREA -------------------------------

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__this_text_area.grid(sticky=N + E + S + W)
        self.__this_text_area.config(yscrollcommand=self.__this_scroll_bar.set)

        # get fired when encounter
        # one of the delimiters
        self.__this_text_area.bind(
            "<KeyRelease>",
            self.call_detection
        )

        # Ctrl+N to Create New
        self.__this_text_area.bind(
            "<Control-Key-n>",
            self.newFile
        )

        # Ctrl+N to Open File
        self.__this_text_area.bind(
            "<Control-Key-o>",
            self.openFile
        )

        # Ctrl+Q to Exit
        self.__this_text_area.bind(
            "<Control-Key-q>",
            self.quitApplication
        )

        # Ctrl+S to Save
        self.__this_text_area.bind(
            "<Control-Key-s>",
            self.saveFile
        )

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

            self.__this_text_area.delete(1.0, END)

            with open(self.__file, 'r') as file:
                self.__this_text_area.insert(1.0, file.read())

    # NEWFILE
    def newFile(self, event=None):

        self.__root.title('Untitled - AutoS-Notepad')
        self.__file = None
        self.__this_text_area.delete(1.0, END)

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
                    file.write(self.__this_text_area.get(1.0, END))

                # Change the window title
                self.__root.title(
                        os.path.basename(self.__file)
                        + ' - Notepad')
        else:
            with open(self.__file, 'w') as file:
                file.write(self.__this_text_area.get(1.0, END))

    def cut(self):
        self.__this_text_area.event_generate('<<Cut>>')

    def copy(self):
        self.__this_text_area.event_generate('<<Copy>>')

    def paste(self):
        self.__this_text_area.event_generate('<<Paste>>')

    # live word detection
    __delimiters = [
        ' ', '.', '!', '?', '\n'
    ]

    def call_detection(self, event):
        key_typed = event.char


        if key_typed in self.__delimiters:
            typed_string = self.__this_text_area.get(1.0, END)
            predict(typed_string, u_model, b_model, t_model)


    def run(self):
        # Run main application
        self.__root.mainloop()


# Run main application
if __name__ == '__main__':
    execfile('Mytest.py')

    notepad = Notepad()
    notepad.run()
