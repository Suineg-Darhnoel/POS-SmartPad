from PosNgram import *

def predict_pos_token(
        ngram_sent,
        *ngram_models,
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

    if len(sent_poses) == 0:
        # employ only unigram
        print("You may try...")

        pos_prob = ngram_models[0].freq2prob().most_common(mc)
        for pos, prob in pos_prob:

            info = "{} with {:.2f}% probability being right."
            print(info.format(pos[-1], prob*100))

            word_pos = ngram_models[0].phi2(pos[-1])
            words = [
                word for word, pos in word_pos
            ]

            random.shuffle(words)
            print("For example: ", words[:3], end="\n\n")

    elif len(sent_poses) == 1:
        # employ unigram and bigram
        freq2prob_data2 = ngram_models[1].freq2prob()
        tp_prob = ngram_models[1].phi2(
            sent_poses,
            default_dict=freq2prob_data2,
            include_values=True
        )

        pos_prob2 = FreqDist()
        for (_, poses), prob in tp_prob:
            pos_prob2.update({poses:prob})

        print("You may try...")

        pos_prob2 = pos_prob2.most_common(3)
        for pos, prob in pos_prob2:

            info = "<{}> with {:.2f}% probability being right."
            print(info.format(pos[-1], prob*100))

            word_pos = ngram_models[0].phi2((pos[-1],))
            words = [
                word for word, pos in word_pos
            ]

            random.shuffle(words)
            print("For example: ", words[:3], end="\n\n")
    else:
        pass


# start testing
if __name__== "__main__":
    filename = "austen-emma.txt"
    size=10**5 # just 1/8 of the whole file
    # size = None

    u_model = PosNgram(1)
    b_model = PosNgram(2)
    t_model = PosNgram(3)

    u_model.freq_counts(filename, size)
    b_model.freq_counts(filename, size)
    t_model.freq_counts(filename, size)
