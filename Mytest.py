filenames = [
    "data/austen-emma.txt",
    "data/science.txt"
]
size = 10**5 # just 1/8 of the whole file
# size = None

u_model = PosNgram(1)
b_model = PosNgram(2)
t_model = PosNgram(3)

u_model.pre_process(*filenames, size=size)
b_model.pre_process(*filenames, size=size)
t_model.pre_process(*filenames, size=size)
