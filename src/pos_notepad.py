import tkinter
import re
import os
import time
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from past.builtins import execfile

from pos_predict import *
import threading


class Notepad:

    def __init__(self, model, **kwargs):
        # set window size
        try:
            self.width = kwargs['width']
        except KeyError:
            pass

        try:
            self.height = kwargs['height']
        except KeyError:
            pass

        # SET UP MODEL
        self.model = model

        # TKINTER ROOT ---------------
        self.root = Tk()
        # default window width and height
        self.width, self.height = 500, 600

        # init text_area
        self.text_area = Text(self.root)

        # init result frame
        self.result_box = Listbox(self.root)


        # MENU BAR
        self.menu_bar = Menu(self.root)
        self.scale_bar = Scale(
                    self.menu_bar,
                    from_=14,
                    to=30,
                    orient='horizontal'
                )
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu = Menu(self.menu_bar, tearoff=0)

        # title
        self.title = 'Smart Pad'
        # To add scrollbar
        self.scroll_bar = Scrollbar(self.text_area)
        self.file = None

        # WINDOW ---------------------

        # Set the window text
        self.root.title(self.title)
        self.img = PhotoImage(file='../images/smart-pad-logo.png')
        self.root.iconphoto(False, self.img)


        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # For left-alling
        left = screen_width/ 2 - self.width / 2

        # For right-allign
        top = screen_height / 2 - self.height / 2

        # For top and bottom
        self.root.geometry('%dx%d+%d+%d'
                % (self.width, self.height, left, top))

        # MENU -------------------------------

        # To open new file
        self.file_menu.add_command(
                label='New',
                command=self.newFile,
                accelerator="Ctrl+N")

        # To open a already existing file
        self.file_menu.add_command(
                label='Open',
                command=self.openFile,
                accelerator="Ctrl+O")

        # To save current file
        self.file_menu.add_command(
                label='Save',
                command=self.saveFile,
                accelerator="Ctrl+S")

        # To create a line in the dialog
        self.file_menu.add_separator()

        self.file_menu.add_command(
                label='Exit',
                command=self.quitApplication,
                accelerator='Ctrl+Q')

        self.menu_bar.add_cascade(
                label='File',
                menu=self.file_menu)

        # To give a feature of cut
        self.edit_menu.add_command(
                label='Cut',
                command=self.cut)

        # to give a feature of copy
        self.edit_menu.add_command(
                label='Copy',
                command=self.copy)

        # To give a feature of paste
        self.edit_menu.add_command(
                label='Paste',
                command=self.paste)

        # To give a feature of editing
        self.menu_bar.add_cascade(
                label='Edit',
                menu=self.edit_menu)

        # To predict
        self.menu_bar.add_command(
                label='Predict',
                command=self.prediction_callback,
                )

        self.menu_bar.config(background='#6e9a44', foreground='white')
        self.menu_bar.config()
        self.root.config(menu=self.menu_bar)


        # SCROLLBAR -------------------------------

        # Scrollbar will adjust automatically according to the content
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.scroll_bar.config(command=self.text_area.yview)

        # TEXTAREA -------------------------------

        # To make the textarea auto resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.text_area.grid(sticky=N + E + S + W)
        self.text_area.config(yscrollcommand=self.scroll_bar.set)

        # Add result (widget)
        self.result_box.grid(sticky=N + E + S + W)

        # set default font size
        self.text_area.config(font=('Time New Roman', 15))
        self.text_area.configure(bg='black', fg='white', insertbackground='white')

        txt_area_binding_list = [
                    ("<KeyRelease-space>", self.realtime_prediction),
                    ("<Control-Key-n>", self.newFile),
                    ("<Control-Key-o>", self.openFile),
                    ("<Control-Key-q>", self.quitApplication),
                    ("<Control-Key-s>", self.saveFile)
                ]

        for ctr_key, func in txt_area_binding_list:
            self.text_area.bind_all(ctr_key, func)

    ############## METHOD ####################

    # QUIT
    def quitApplication(self, event=None):
        self.root.destroy()

    # OPENFILE
    def openFile(self, event=None):

        self.file = askopenfilename(
                defaultextension='.txt',
                filetypes=[
                    ('All Files', '*.*'),
                    ('Text Documents','*.txt')
                    ]
                )

        if self.file == '':
            # no file to open
            self.file = None
        else:
            # Try to open the file
            # set the window title
            notepad_name = ' Smart Pad'
            self.root.title(
                    os.path.basename(self.file)
                    + notepad_name)

            self.text_area.delete(1.0, END)

            with open(self.file, 'r') as file:
                self.text_area.insert(1.0, file.read())

    # NEWFILE
    def newFile(self, event=None):

        self.root.title('Smart Pad')
        self.file = None
        self.text_area.delete(1.0, END)

    # SAVEFILE
    def saveFile(self, event=None):

        if self.file == None:

            # Save as new file
            self.file = asksaveasfilename(
                    initialfile='Untitled.txt',
                    defaultextension='.txt',
                    filetypes=[
                        ('All Files','*.*'),
                        ('Text Documents', '*.txt')
                        ]
                    )

            if self.file == '':
                self.file = None
            else:

                # Try to save the file
                with open(self.file, 'w') as file:
                    file.write(self.text_area.get(1.0, END))

                # Change the window title
                self.root.title(
                        os.path.basename(self.file)
                        + ' - Notepad')
        else:
            with open(self.file, 'w') as file:
                file.write(self.text_area.get(1.0, END))

    # TEXT MANIPULATION

    def cut(self):
        self.text_area.event_generate('<<Cut>>')

    def copy(self):
        self.text_area.event_generate('<<Copy>>')

    def paste(self):
        self.text_area.event_generate('<<Paste>>')

    # TEXT RESIZING
    def resize_font(self, event=None):
        self.text_area.config(
                    font=(
                            'Time New Roman',
                            self.scale_bar.get()
                        )
                )

    # prediction_callback is called whenever key is released
    def prediction_callback(self):
        curr_text = self.text_area.get(1.0, END);
        predict_result = self.model.predict(curr_text)

        try:
            self.result_box.delete(0, END);
            for part_of_speech, words in predict_result:
                tmp_text = "[ {} ]: {}".format(part_of_speech, ",".join(words))
                self.result_box.insert("end", tmp_text)
        except TypeError:
            pass

    # realtime prediction
    def realtime_prediction(self, event=None):
        t = threading.Thread(target=self.prediction_callback)
        t.start()

    def run(self):
        # Run main application
        self.root.mainloop()


