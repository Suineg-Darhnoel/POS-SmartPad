from PosNgram import *
from PosMapping import poscode2word
from past.builtins import execfile
import math
import time
import random


class Predict:

    def __init__(
            self,
            context,
            model_nums=3,
            t_size=90
        ):
        assert model_nums >= 2
        self.ng_models = [
                PosNgram(i)
                for i in range(1, model_nums+1)
            ]
        for model in self.ng_models:
            model.pre_process(context, training_size=t_size)

        self.poses2suggest = FreqDist()

    def prior_probs(self, sentence, model, word_nums=5):
        sentence = sentence.lower()
        sents = word_tokenize(sentence)
        sents = sents[-word_nums:]

        token_pos_ngram = ngrams(
                    pos_tag(sents),
                    model.order
                )

        log_probs = []
        for elem in token_pos_ngram:
            pos = tuple((r for _, r in elem))

            data = model.fetch_if("prefix", pos[:-1])
            n = data[pos]
            d = data.N()

            if d == 0 or n == 0:
                log_probs.append(-10**10)
                continue
            print(pos, n/d)
            log_probs.append(math.log(n/d))

        # sum of log is log of multiplication
        log_prob_sum = sum(log_probs)

        # the sentence contains the word to which
        # there is no the correspoding pos
        if log_prob_sum == 0:
            return 0

        return math.e**log_prob_sum

    def last_token2pos_token(self, last_token, model):
        tmp_data = model.fetch_if(
                'prefix',
                last_token,
                pos_is_target=False,
                include_pair=True
            )

        pos_token_freq = dict()
        for (word, pos), freq in tmp_data.items():
            if pos[-1] not in pos_token_freq:
                pos_token_freq[pos[-1]] = FreqDist()
            pos_token_freq[pos[-1]].update({word[-1]:freq})

        pos_freq_token = dict()
        for pos, token_freq in pos_token_freq.items():
            pos_freq_token[pos] = dict()
            for token, freq in token_freq.items():
                if freq not in pos_freq_token[pos]:
                    pos_freq_token[pos][freq] = []
                pos_freq_token[pos][freq].append(token)

        return pos_freq_token

    def ngram_test(self, order):
        # >>> conduct testing on bigram
        # >>> conduct testing on trigram
        # >>> conduct testing on bigram + trigram
        # trigram + brigram
        # testing's starting time
        start_testing = time.time()

        for sent in self.ng_models[1].test_sents:
            sentence = " ".join(sent).lower()
            pos_tag_ngram = ngrams(pos_tag(word_tokenize(sentence)), order)

            for token_poses in pos_tag_ngram:
                pos = tuple()
                for _, p in token_poses:
                    pos += (p,)
                print(pos)
        # end of testing
        print("exec time = {}".format(time.time()-start_testing))

    def predict(
            self,
            sentence,
            mc=3,
        ):
        start_predicting = time.time()

        #########################################################

        # PREPROCESS
        sentence = sentence.lower()

        tokenized_words = word_tokenize(sentence)
        sent_token_pos = pos_tag(tokenized_words[-5:])
        # print(sent_token_pos)

        sent_tokens = tuple(token for token, _ in sent_token_pos[-2:])
        sent_poses = tuple(pos for _, pos in sent_token_pos[-2:])

        b_model = self.ng_models[1]

        #########################################################

        # TRY IF THE THE LAST TOKEN EXISTS IN BIGRAM
        last_token = tuple(sent_tokens[-1:])
        # print('last token is: ', last_token)

        #########################################################
        epsilon = 0.001
        self.poses2suggest = FreqDist()

        if len(sent_poses) == 1:
            # bigram model
            all_poses_freq_in_b = \
                    b_model.fetch_if('prefix', sent_poses[-1:])
            d = all_poses_freq_in_b.N() + epsilon
            for p, freq in all_poses_freq_in_b.items():
                n = freq
                self.poses2suggest.update({p[-1]:n/d})

        elif len(sent_poses) == 2:
            # bigram + trigram model
            t_model = self.ng_models[2]
            the_pos_suffix = sent_poses[-1:]

            all_poses_freq_in_b = \
                    b_model.fetch_if('prefix', the_pos_suffix)
            all_poses_freq_in_t = \
                    t_model.fetch_if('prefix', sent_poses)

            db = all_poses_freq_in_b.N() + epsilon
            for pos_b, freq_b in all_poses_freq_in_b.items():
                p, pb, pt = 0, 0, 0

                nb = freq_b
                pb = nb / db

                pos_t = tuple()
                for x in all_poses_freq_in_t:
                    if x[-len(pos_b):] == pos_b:
                        pos_t = x

                if pos_t:
                    nt = all_poses_freq_in_t[pos_t]
                    dt = t_model.fetch_if('prefix', pos_t[:-1]).N() + epsilon
                    pt = nt / dt

                # interpolation
                p = 0.2 * pb + 0.8 * pt
                if pos_b[-1] not in self.poses2suggest:
                    self.poses2suggest.update({pos_b[-1] : p})

        ##########################################################
        ## PRINT
        print_info = "----------< {} >----------"+\
                     "\nwith estimated probability ~ {:.2f}%"
        print("\nYou may try...")

        # last_token to pos_token = lt2pt
        lt2pt = self.last_token2pos_token((last_token),b_model)
        total_freqs_lt2pt = 0
        for pos, vals in lt2pt.items():
            total_freqs_lt2pt += sum(vals)

        # print(total_freqs_lt2pt)

        final_pos_score = FreqDist()
        if lt2pt:
            for pos, prob in self.poses2suggest.items():
                if pos not in lt2pt:
                    res = 0
                else:
                    res = sum(lt2pt[pos])/total_freqs_lt2pt
                    final_pos_score.update({pos: 100* prob * res})
        # final_pos_score.pprint()

        result = final_pos_score.most_common(3)

        # 1st: Suggest words from Bigram's dictionary
        # 2nd: If there is no word in the Bigram, just
        # randomly apply POS to suggest words

        if len(result) < 3:
            print("len(result) < 3")
            result = self.poses2suggest.most_common(mc)

            for pos, score in result:

                print(print_info.format(poscode2word(pos), score))
                words = list(self.ng_models[0].poses2tokens((pos,)))

                words2suggest = random.sample(
                    words, min(len(words), 4)
                )

                words2suggest = [x[0] for x in words2suggest]
                for word in words2suggest:
                    print(">>> " + word)
        else:
            max_word = 3
            for pos, score in result:
                suggest_words = lt2pt[pos]
                sorted_words = sorted(suggest_words)

                print(print_info.format(poscode2word(pos), score))
                final_words = []
                for index in sorted_words:
                    for w in suggest_words[index][:max_word]:
                        final_words.append(w)

                words2suggest = random.sample(
                    final_words, min(len(final_words), 4)
                )

                for word in words2suggest:
                    print(">>> " + word)

        print("<>"*20)
        # end of predicting
        print("exec time = {}".format(time.time()-start_predicting))

        #########################################################


# start testing
if __name__== "__main__":
    pass
