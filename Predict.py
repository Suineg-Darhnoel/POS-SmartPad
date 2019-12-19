from PosNgram import *
from PosMapping import poscode2word
from past.builtins import execfile
import time
import random

def predict(
        ngram_sent,
        *ng_models,
        mc=3,
        timer=False
    ):

    def ptf_dict(dict_data):
        # ptf stands for pos__token_freq
        tmp_dict = dict()
        for (t, p), f in dict_data.items():
            if p not in tmp_dict:
                tmp_dict[p] = FreqDist()
            tmp_dict[p].update({p:f})
        return tmp_dict

    def ngram_prob(term, model, target_dict=None):
        if target_dict is None:
            target_dict = model.ngram_data
        pass
    #########################################################

    # PREPROCESS
    start = time.time()
    ngram_sent = ngram_sent.lower()
    sent_token_pos = pos_tag(
        word_tokenize(ngram_sent)
    )
    # print(sent_token_pos)

    sent_tokens = tuple(token for token, _ in sent_token_pos[-2:])
    sent_poses = tuple(pos for _, pos in sent_token_pos[-2:])

    b_model = ng_models[1]

    #########################################################

    # TRY IF THE THE LAST TOKEN EXISTS IN BIGRAM
    last_token = tuple(sent_tokens[-1:])
    print('last token is: ', last_token)

    token_freq = b_model.fetch_if(
            'prefix',
            last_token,
            pos_is_target=False,
            include_pair=True
        )

    for d in token_freq.items():
        print(d)

    #########################################################
    epsilon = 0.001
    poses2suggest = FreqDist()

    #if len(sent_poses) == 1:
    #    # bigram model
    #    all_poses_freq_in_b = b_model.fetch_if('prefix', sent_poses)
    #    for p, freq in all_poses_freq_in_b.items():
    #        n = freq
    #        d = b_model.fetch_if('prefix', p[:-1]).N() + epsilon
    #        poses2suggest.update({p[-1]:n/d})

    #elif len(sent_poses) == 2:
    #    # bigram + trigram model
    #    t_model = ng_models[2]
    #    the_pos_suffix = sent_poses[-1:]

    #    all_poses_freq_in_b = b_model.fetch_if('prefix', the_pos_suffix)
    #    all_poses_freq_in_t = t_model.fetch_if('prefix', sent_poses)

    #    for pos_b, freq_b in all_poses_freq_in_b.items():
    #        p, pb, pt = 0, 0, 0

    #        nb = freq_b
    #        db = b_model.fetch_if('prefix', pos_b[:-1]).N() + epsilon
    #        pb = nb / db

    #        pos_t = tuple()
    #        for x in all_poses_freq_in_t:
    #            if x[-len(pos_b):] == pos_b:
    #                pos_t = x

    #        if pos_t:
    #            nt = all_poses_freq_in_t[pos_t]
    #            dt = t_model.fetch_if('prefix', pos_t[:-1]).N() + epsilon
    #            pt = nt / dt

    #        # interpolation
    #        p = 0.2 * pb + 0.8 * pt
    #        if pos_b[-1] not in poses2suggest:
    #            poses2suggest.update({pos_b[-1] : p})

    ##########################################################
    ## PRINT
    #print_info = "----------< {} >----------"+\
    #             "\nwith {:.2f}% probability being right."
    #print("\nYou may try...")

    #result = poses2suggest.most_common(mc)
    #for pos, prob in result:

    #    print(print_info.format(poscode2word(pos), prob*100))
    #    words = list(ng_models[0].poses2tokens((pos,)))
    #    words2suggest = random.sample(
    #        words, min(len(words), 4)
    #    )

    #    words2suggest = [x[0] for x in words2suggest]
    #    toprint = ""
    #    for word in words2suggest:
    #        toprint = ">>> " + word
    #        print(toprint)

    # 1st: Suggest words from Bigram's dictionary
    # 2nd: If there is no word in the Bigram, just
    # randomly apply POS to suggest words

    # if timer:
    #     print('exec_time: ', time.time()-start)
    print("<>"*20)

    #########################################################

# start testing
if __name__== "__main__":
    execfile('Mytest.py')
