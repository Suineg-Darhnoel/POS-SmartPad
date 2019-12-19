filenames = [
    "data/austen-emma.txt",
    "data/science.txt"
]
size = 10**4
# size = None

u_model = PosNgram(1)
b_model = PosNgram(2)
t_model = PosNgram(3)

u_model.pre_process(filenames[1], size=size)
b_model.pre_process(filenames[1], size=size)
t_model.pre_process(filenames[1], size=size)
