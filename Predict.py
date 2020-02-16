from PosNgram import *
from PosMapping import poscode2word
from past.builtins import execfile
from termcolor import colored
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

        self._poses2suggest = FreqDist()

    # This function is used for prior probability calculation
    # of the sequence of POS obtained from the given sentence
    def prior_probs(self, sentence, model, word_nums=5):
        sentence = sentence
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

    # This function is used to suggest the next word
    # based on bigram
    def bigram2pos_token(self, last_token, model):
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

    def find_pos_rank(self, arg):
        mst_common = self._poses2suggest.most_common()
        for k, (pos, _) in enumerate(mst_common):
            if arg == pos:
                return k
        return len(mst_common)

    # conduct testing on bigram + trigram
    def pos_ngram_test(self, sug_nums = 3):
        start_testing = time.time()

        total_rank = 0
        total = 0
        correct = 0

        for sent in self.ng_models[1].test_sents:

            sentence = " ".join(sent)
            pos_tag_ngram = ngrams(pos_tag(word_tokenize(sentence)), 3)

            for token_poses in pos_tag_ngram:
                gram_s = time.time()
                token, pos = tuple(), tuple()
                for t, p in token_poses:
                    pos += (p,)
                    token += (t,)
                print("<>"*30)

                self.update_suggestion(pos[:-1])
                most_common3 = {
                        fst for fst, snd
                        in self._poses2suggest.most_common(sug_nums)
                    }

                curr_pos = pos[-1]
                verbal_message1 = "Ground Truth : <{}> -> Suggest : {}"
                print(verbal_message1.format(curr_pos, most_common3))

                total += 1
                if curr_pos in most_common3:
                    correct += 1

                accuracy = 100 * (correct / total)
                print("accuracy = {:.2f}%, total = {}".format(accuracy, total))

                curr_rank = self.find_pos_rank(curr_pos)
                total_rank += curr_rank
                ranking_ratio = total_rank / total

                verbal_message2 = "<{}>'s rank = {}, average_ranking = {}'"
                print(verbal_message2.format(curr_pos, curr_rank, ranking_ratio))

                gram_e = time.time()
                print("exec time = {}".format(gram_e - gram_s))
        # end of testing
        print("exec time = {}".format(time.time()-start_testing))

    def update_suggestion(self, sent_poses):
        b_model = self.ng_models[1]

        # initialize _poses2suggest data
        self._poses2suggest = FreqDist()

        if len(sent_poses) == 1:
            # apply bigram model only
            all_poses_freq_in_b = \
                    b_model.fetch_if('prefix', sent_poses[-1:])
            d = all_poses_freq_in_b.N()

            for p, freq in all_poses_freq_in_b.items():
                n = freq
                self._poses2suggest.update({p[-1]:n/d})

        elif len(sent_poses) == 2:
            # APPLY BIGRAM AND TRIGRAM MODEL
            t_model = self.ng_models[2]
            the_pos_suffix = sent_poses[-1:]

            all_poses_freq_in_b = \
                    b_model.fetch_if('prefix', the_pos_suffix)
            all_poses_freq_in_t = \
                    t_model.fetch_if('prefix', sent_poses)

            db = all_poses_freq_in_b.N()
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
                    dt = t_model.fetch_if('prefix', pos_t[:-1]).N()
                    pt = nt / dt

                # INTERPOLATION
                p = 0.2 * pb + 0.8 * pt
                if pos_b[-1] not in self._poses2suggest:
                    self._poses2suggest.update({pos_b[-1] : p})

    def sent2sent_token_pos(self, sentence):
        # lowerify all the character in the given sentence
        # sentence = sentence.lower()

        tokenized_words = word_tokenize(sentence)
        sent_token_pos = pos_tag(tokenized_words[-5:])

        sent_tokens = tuple(token for token, _ in sent_token_pos[-2:])
        sent_poses = tuple(pos for _, pos in sent_token_pos[-2:])

        return sent_tokens, sent_poses

    def predict(
            self,
            sentence,
            mc=3,
        ):
        #########################################################
        print_info = "----------< {} >----------"
                     # "\nwith estimated probability ~ {:.2f}%"
        colored_info = colored(
                        print_info,
                        "blue",
                        attrs=['bold', 'underline']
                    )

        oov_message = "-- OOV -> Random Suggest --"
        oov_alert = colored(oov_message, "red",attrs=['bold', 'blink'])
        #########################################################
        start_predicting = time.time()
        b_model = self.ng_models[1]

        sent_tokens, sent_poses =\
                self.sent2sent_token_pos(sentence)

        #########################################################
        # update pos suggestion list
        self.update_suggestion(sent_poses)

        #########################################################
        # TRY IF THE THE LAST TOKEN EXISTS IN BIGRAM
        last_token = tuple(sent_tokens[-1:])
        # print('last token is: ', last_token)

        ##########################################################

        # last_token to pos_token = lt2pt
        lt2pt = self.bigram2pos_token((last_token),b_model)
        total_freqs_lt2pt = 0
        for pos, vals in lt2pt.items():
            total_freqs_lt2pt += sum(vals)

        # print(total_freqs_lt2pt)

        final_pos_score = FreqDist()
        if lt2pt:
            for pos, prob in self._poses2suggest.items():
                if pos not in lt2pt:
                    res = 0
                else:
                    res = sum(lt2pt[pos])/total_freqs_lt2pt
                    final_pos_score.update({pos: 100 * prob * res})
        # final_pos_score.pprint()

        result = final_pos_score.most_common(3)

        #########################################################
        # 1st: Suggest words from Bigram's dictionary
        # 2nd: If there is no word in the Bigram, just
        # randomly apply POS to suggest words
        col_msg = colored("\nYou may try", "green", attrs=['bold'])
        propose_msg = '<>'*20 + col_msg
        print(propose_msg + colored('...', attrs=['blink']))

        if len(result) < 3:
            # print("len(result) < 3")
            # -- OOV ALERT --
            print(oov_alert)

            result = self._poses2suggest.most_common(mc)

            for pos, _ in result:

                prob_res = self._poses2suggest[pos] * 100
                print(colored_info.format(poscode2word(pos)))
                words = list(self.ng_models[0].poses2tokens((pos,)))

                words2suggest = random.sample(
                    words, min(len(words), 4)
                )

                words2suggest = [x[0] for x in words2suggest]
                for word in words2suggest:
                    print(">>> " + word)
        else:
            max_word = 3
            for pos, prob in result:
                suggest_words = lt2pt[pos]
                sorted_words = sorted(suggest_words)

                print(colored_info.format(poscode2word(pos)))
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


# start testing
if __name__== "__main__":
    pass
