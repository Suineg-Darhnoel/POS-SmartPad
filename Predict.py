from PosNgram import *

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
        pos for _, pos in sent_token_pos[-1:]
    ])

    print(sent_poses)

    if len(sent_poses) == 1:
        print_info = "<{}> with {:.2f}% probability being right."
        # bigram model

        the_pos = tuple(sent_poses)
        all_poses = ng_models[1].fetch_if_head(
                the_pos, ng_models[0])
        print(all_poses)

        next_pos_prob = FreqDist()

        for p in all_poses:
            n = ng_models[1].joint_freq(p)
            d = ng_models[0].joint_freq(p[:-1])
            next_pos_prob.update({p[-1]:n/d})

        print("You may try...")
        result = next_pos_prob.most_common(5)
        print(result)

        for pos, prob in result:

            print(print_info.format(pos, prob*100))

            # random.shuffle(words)
            # print("For example: ", words[:3], end="\n\n")
    else:
        # trigram model
        pass


# start testing
if __name__== "__main__":
    filename = "austen-emma.txt"
    size=10**4 # just 1/8 of the whole file
    # size = None

    u_model = PosNgram(1)
    b_model = PosNgram(2)
    t_model = PosNgram(3)

    u_model.freq_counts(filename, size)
    b_model.freq_counts(filename, size)
    t_model.freq_counts(filename, size)
