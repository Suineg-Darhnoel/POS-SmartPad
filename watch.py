import os
import sys
import subprocess as subp

if len(sys.argv) < 2:
    filename = "slide.tex"
else:
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        sys.exit("file: "+ filename +" not found")

f = os.path.getmtime(filename)
actual_fname = filename.split(".tex")[0]

subp.run("pdflatex " + filename, shell=True)
subp.run("xdg-open " + actual_fname + ".pdf", shell=True)

while True:
    nf = os.path.getmtime(filename)
    if  nf != f:
        subp.run("pdflatex "+ filename, shell=True)
        f = nf
