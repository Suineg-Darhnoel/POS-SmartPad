#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter
import re
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from testing import *

class Notepad:

    __root = Tk()

    # default window width and height
    __thisWidth = 400
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)

    # title
    __title = 'Untitled - AutoS-Notepad'
    # To add scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

    def __init__(self, **kwargs):
        # set window size
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # WINDOW -------------------------------

        # Set the window text
        self.__root.title(self.__title)

        # Center the window
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()

        # For left-alling
        left = screen_width/ 2 - self.__thisWidth / 2

        # For right-allign
        top = screen_height / 2 - self.__thisHeight / 2

        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d'
                % (self.__thisWidth,
                   self.__thisHeight, left, top))

        # MENU -------------------------------

        # To open new file
        self.__thisFileMenu.add_command(
                label='New',
                command=self.newFile,
                accelerator="Ctrl+N")

        # To open a already existing file
        self.__thisFileMenu.add_command(
                label='Open',
                command=self.openFile,
                accelerator="Ctrl+O")

        # To save current file
        self.__thisFileMenu.add_command(
                label='Save',
                command=self.saveFile,
                accelerator="Ctrl+S")

        # To create a line in the dialog
        self.__thisFileMenu.add_separator()

        self.__thisFileMenu.add_command(label='Exit',
                command=self.quitApplication,
                accelerator='Ctrl+Q')

        self.__thisMenuBar.add_cascade(label='File',
                menu=self.__thisFileMenu)

        # To give a feature of cut
        self.__thisEditMenu.add_command(
                label='Cut',
                command=self.cut)

        # to give a feature of copy
        self.__thisEditMenu.add_command(
                label='Copy',
                command=self.copy)

        # To give a feature of paste
        self.__thisEditMenu.add_command(
                label='Paste',
                command=self.paste)

        # To give a feature of editing
        self.__thisMenuBar.add_cascade(
                label='Edit',
                menu=self.__thisEditMenu)

        self.__root.config(menu=self.__thisMenuBar)

        # SCROLLBAR -------------------------------

        # Scrollbar will adjust automatically according to the content
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)

        # TEXTAREA -------------------------------

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__thisTextArea.grid(sticky=N + E + S + W)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

        # get fired when encounter
        # one of the delimiters
        self.__thisTextArea.bind(
            "<KeyRelease>",
            self.call_detection
        )

        # Ctrl+N to Create New
        self.__thisTextArea.bind(
            "<Control-Key-n>",
            self.newFile
        )

        # Ctrl+N to Open File
        self.__thisTextArea.bind(
            "<Control-Key-o>",
            self.openFile
        )

        # Ctrl+Q to Exit
        self.__thisTextArea.bind(
            "<Control-Key-q>",
            self.quitApplication
        )

        # Ctrl+S to Save
        self.__thisTextArea.bind(
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

            self.__thisTextArea.delete(1.0, END)

            with open(self.__file, 'r') as file:
                self.__thisTextArea.insert(1.0, file.read())

    # NEWFILE
    def newFile(self, event=None):

        self.__root.title('Untitled - AutoS-Notepad')
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

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
                    file.write(self.__thisTextArea.get(1.0, END))

                # Change the window title
                self.__root.title(
                        os.path.basename(self.__file)
                        + ' - Notepad')
        else:
            with open(self.__file, 'w') as file:
                file.write(self.__thisTextArea.get(1.0, END))

    def cut(self):
        self.__thisTextArea.event_generate('<<Cut>>')

    def copy(self):
        self.__thisTextArea.event_generate('<<Copy>>')

    def paste(self):
        self.__thisTextArea.event_generate('<<Paste>>')

    # live word detection
    __delimiters = [
        ' ', '.', '!', '?', '\n'
    ]

    def call_detection(self, event):
        key_typed = event.char

        if key_typed == ' ':
            text = self.__thisTextArea.get(-3.0, END)
            # print("after space: ", text)


        if key_typed in self.__delimiters:
            typed_string = self.__thisTextArea.get(1.0, END)
            predict_pos_token(typed_string, u_model, b_model)


    def run(self):
        # Run main application
        self.__root.mainloop()


# Run main application
if __name__ == '__main__':
    from Predict import *
    filename = "austen-emma.txt"
    size=10**4 # just 1/8 of the whole file
    # size = None

    u_model = PosNgram(1)
    b_model = PosNgram(2)
    t_model = PosNgram(3)

    u_model.freq_counts(filename, size)
    b_model.freq_counts(filename, size)
    t_model.freq_counts(filename, size)

    notepad = Notepad()
    notepad.run()
