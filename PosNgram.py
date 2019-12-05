from math import log
from math import exp
from nltk import ngrams, pos_tag, word_tokenize, FreqDist
import random


class PosNgram():

    def __init__(self, deg=1):
        self.degree = deg
        self.__sentence = ""

        # storing tokens and frequency
        self.ngram_data = FreqDist()

        # to prevent from illegral argument
        if deg < 1:
            self.degree = 1

    def poses2tokens(
            self,
            pos_terms,
            include_freq=False,
            default_dict=None
        ):
        """
        # The token_terms must be the element of ngram_model
        # whose degree is 1 smaller than that of the current one.
        """
        if default_dict is None:
            default_dict = self.ngram_data

        for (tokens, poses), freq in default_dict.items():
            if self.degree > 1:
                tmp_poses = poses[:self.degree-1]
            else:
                tmp_poses = poses
            if pos_terms == tmp_poses:
                yield tokens if\
                        not include_freq\
                        else (tokens, freq)

    def tokens2poses(
            self,
            token_terms,
            include_freq=False,
            default_dict=None
        ):
        """
        # The token_terms must be the element of ngram_model
        # whose degree is 1 smaller than that of the current one.
        """
        if default_dict is None:
            default_dict = self.ngram_data

        for (tokens, poses), freq in default_dict.items():
            if self.degree > 1:
                tmp_tokens = tokens[:self.degree-1]
            else:
                tmp_tokens = tokens
            if token_terms == tmp_tokens:
                yield poses if\
                        not include_freq\
                        else (poses, freq)

    def freq_counts(
            self,
            filename,
            size=None,
        ):

        self.ngram_data = FreqDist()
        with open(
                filename,
                encoding="utf-8",
                errors="ignore"
            ) as fptr:

            lines = fptr.readlines(size)

        for line in lines:
            self.__sentence = line.lower()

            # Counting Step
            self.ngram_data.update(self.__token_pos_pairs)

    def freq2prob(
            self,
            include_token=True
        ):
        # need to improve !!!!!!!!!
        ngram_probs = FreqDist()

        if include_token:
            for elem in self.ngram_data:
                ngram_probs.update(
                    {elem : self.ngram_data.freq(elem)}
                )
        else:
            new_ngram_data = FreqDist()
            for elem in self.ngram_data:
                new_ngram_data.update(
                    {elem[1]}
                )

            for elem in new_ngram_data:
                ngram_probs.update(
                    {elem : new_ngram_data.freq(elem)}
                )

        return ngram_probs

    def joint_freq(self, pos):
        def is_similar(w1, w2):
            w1 = list(w1)
            w2 = list(w2)
            assert len(w1) == len(w2)
            for w in w1:
                if w in w2:
                    w2.remove(w)
            if len(w2) == 0:
                return True
            return False

        tmp_freq = 0
        for (_, p), freq in self.ngram_data.items():
            if is_similar(pos, p):
                tmp_freq += 1

        return tmp_freq

    @property
    def __token_pos_pairs(self):
        """
        This function maps terms to POS
        (The previous version's name was phi1)
        """
        for elems in self.__ngram_tokens_pos:
            poses = [elem[1] for elem in elems]

            tokens = [elem[0] for elem in elems]
            yield (tuple(tokens), tuple(poses))

    @property
    def __sent2pos_tag(self):
        sent = self.__sentence.lower()
        tokens = word_tokenize(sent)
        return pos_tag(tokens)

    @property
    def __ngram_tokens_pos(self):
        # this returns the tuples of token pos pair
        return ngrams(
            self.__sent2pos_tag,
            self.degree
        )

    def show_prob_info(self, mc=10, include_token=False):
        for elem in self.freq2prob(include_token).most_common(mc):
            print(elem)

if __name__ == '__main__':
    # testing
    filename = "austen-emma.txt"
    size=10**4 # just 1/8 of the whole file
    # size = None

    u_model = PosNgram(1)
    b_model = PosNgram(2)
    t_model = PosNgram(3)

    u_model.freq_counts(filename, size)
    b_model.freq_counts(filename, size)
    t_model.freq_counts(filename, size)
