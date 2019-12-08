from PosNgram import *
from PosMapping import poscode2word
import time
import random

def predict(
        ngram_sent,
        *ng_models,
        mc=3,
        timer=False
    ):

    #########################################################

    # PREPROCESS
    start = time.time()
    ngram_sent = ngram_sent.lower()
    sent_token_pos = pos_tag(
        word_tokenize(ngram_sent)
    )

    # print(sent_token_pos)
    sent_poses = tuple([
        # need to update later
        pos for _, pos in sent_token_pos[-2:]
    ])

    the_pos = tuple(sent_poses)

    #########################################################

    poses2suggest = FreqDist()

    #########################################################

    if len(sent_poses) == 1:
        # bigram model
        b_model = ng_models[1]
        all_poses_in_b = b_model.fetch_if_prefix(the_pos)

        for p in all_poses_in_b:
            n = b_model.freq_count(p)
            d = sum([
                b_model.freq_count(b)
                for b in b_model.fetch_if_prefix(p[:-1])
            ])
            poses2suggest.update({p[-1]:n/d})

    elif len(sent_poses) == 2:
        # bigram + trigram model
        the_pos_suffix = the_pos[-1:]
        b_model = ng_models[1]
        t_model = ng_models[2]

        all_poses_in_b = b_model.fetch_if_prefix(the_pos_suffix)
        all_poses_in_t = t_model.fetch_if_prefix(the_pos)

        for pos_b in all_poses_in_b:
            p, pb, pt = 0, 0, 0

            nb = b_model.freq_count(pos_b)
            db = sum([
                b_model.freq_count(b)
                for b in b_model.fetch_if_prefix(pos_b[:-1])
            ])

            pb = nb / db

            pos_t = tuple()
            for x in all_poses_in_t:
                if x[-len(pos_b):] == pos_b:
                    pos_t = x

            if pos_t:
                nt = t_model.freq_count(pos_t)
                dt = sum([
                    t_model.freq_count(t)
                    for t in t_model.fetch_if_prefix(pos_t[:-1])
                ])
                pt = nt / dt

            # interpolation
            p = 0.2 * pb + 0.8 * pt
            if pos_b[-1] not in poses2suggest:
                poses2suggest.update({pos_b[-1] : p})

    #########################################################
    # PRINT
    print_info = "----------< {} >----------"+\
                 "\nwith {:.2f}% probability being right."
    print("\nYou may try...")

    result = poses2suggest.most_common(mc)

    for pos, prob in result:

        print(print_info.format(poscode2word(pos), prob*100))
        words = list(ng_models[0].poses2tokens((pos,)))
        words2suggest = random.sample(
            words, min(len(words), 4)
        )

        words2suggest = [x[0] for x in words2suggest]
        toprint = ""
        for word in words2suggest:
            toprint = ">>> " + word
            print(toprint)

    if timer:
        print('exec_time: ', time.time()-start)
    print("<>"*20)

    #########################################################

# start testing
if __name__== "__main__":

    test_files = [
        "data/austen-emma.txt",
        "data/science.txt"
    ]

    size = 10**4 # just 1/8 of the whole file

    u_model = PosNgram(1)
    b_model = PosNgram(2)
    t_model = PosNgram(3)

    u_model.pre_process(test_files[1], size=size)
    b_model.pre_process(test_files[1], size=size)
    t_model.pre_process(test_files[1], size=size)
