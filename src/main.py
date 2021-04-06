#!/usr/bin/python
# -*- coding: utf-8 -*-
from notepad import *
from predict import *

# Run main application
if __name__ == '__main__':
    model = Predict("austen-emma.txt", t_size=50, mc=5)
    model.set_using_console(False) # skip printing to console

    notepad = Notepad(model)
    notepad.run()
