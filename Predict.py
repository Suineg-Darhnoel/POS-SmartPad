from PosNgram import *
import random

def predict_pos_token(
        ngram_sent,
        *ng_models,
        mc=3
    ):

    ngram_sent = ngram_sent.lower()
    sent_token_pos = pos_tag(
        word_tokenize(ngram_sent)
    )

    sent_poses = tuple([
        # need to update later
        pos for _, pos in sent_token_pos[-2:]
    ])

    # print(sent_poses)
    print_info = "<{}> with {:.2f}% probability being right."
    next_pos_prob = FreqDist()
    the_pos = tuple(sent_poses)

    print("You may try ... ")

    if len(sent_poses) == 1:
        # bigram model
        all_poses_in_b = ng_models[1].fetch_if_prefix(the_pos)

        for p in all_poses_in_b:
            n = ng_models[1].freq_count(p)
            d = ng_models[0].freq_count(p[:-1])
            next_pos_prob.update({p[-1]:n/d})

        print("You may try...")
        result = next_pos_prob.most_common(3)
        # print(result)

        for pos, prob in result:

            print(print_info.format(pos, prob*100))
            words = list(ng_models[0].poses2tokens((pos,)))
            words2suggest = random.sample(
                words, min(len(words), 4)
            )

            print("For example: ", *words2suggest)
    elif len(sent_poses) == 2:
        # trigram model
        the_pos_suffix = the_pos[-1:]
        all_poses_in_b = ng_models[1].fetch_if_prefix(the_pos_suffix)
        all_poses_in_t = ng_models[2].fetch_if_prefix(the_pos)
        # print(1, all_poses_in_b)
        # print(2, all_poses_in_t)

        poses2suggest = FreqDist()
        for pos_b in all_poses_in_b:
            # backoff
            p, pb, pt = 0, 0, 0

            nb = ng_models[1].freq_count(pos_b)
            db = ng_models[0].freq_count(pos_b[:-1])
            pb = nb / db

            matched_t_pos = tuple()
            for x in all_poses_in_t:
                if x[-len(pos_b):] == pos_b:
                    matched_t_pos= x
            # print(matched_t_pos)

            if matched_t_pos:
                nt = ng_models[2].freq_count(matched_t_pos)
                dt = ng_models[1].freq_count(matched_t_pos[:-1])
                pt = nt / dt

            p = 0.1 * pb + 0.9 * pt
            # print(pb, pt)
            if pos_b[-1] not in poses2suggest:
                poses2suggest.update({pos_b[-1] : p})

        result = poses2suggest.most_common(3)
        for pos, prob in result:

            print(print_info.format(pos, prob*100))
            words = list(ng_models[0].poses2tokens((pos,)))
            words2suggest = random.sample(
                words, min(len(words), 4)
            )

            print("For example: ", *words2suggest)

# start testing
if __name__== "__main__":
    filename = "austen-emma.txt"
    size=10**5 # just 1/8 of the whole file
    # size = None
    # predict_pos_token('Frankly, I study')

    u_model = PosNgram(1)
    b_model = PosNgram(2)
    t_model = PosNgram(3)

    u_model.pre_process(filename, size)
    b_model.pre_process(filename, size)
    t_model.pre_process(filename, size)
