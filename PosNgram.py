from math import inf
from math import log
from math import exp
from nltk import ngrams, pos_tag, word_tokenize, FreqDist
import random


class PosNgram():

    def __init__(self, ngram=1):
        self.ngram = ngram
        self.__sentence = ""

        # storing tokens and frequency
        self.ngram_dict = FreqDist()

        # to prevent from illegral argument
        if ngram < 1:
            self.ngram = 1

    def __phi1(
            self,
        ):
        """
        This function maps terms to POS
        """
        for elems in self.__ngram_tokens_pos:
            poses = [elem[1] for elem in elems]

            tokens = [elem[0] for elem in elems]
            yield (tuple(tokens), tuple(poses))

    def phi2(
            self,
            terms,
            is_pos=True,
            include_values=False,
            default_dict=None
        ):
        """
        This function maps terms to their
        correspoding pos or vice versa
        It works as a search function
        looking for terms in the dictionary
        """
        if default_dict is None:
            default_dict = self.ngram_dict

        if is_pos:
            for (tokens, poses), freq in default_dict.items():
                if self.ngram > 1:
                    tmp_poses = poses[:self.ngram-1]
                else:
                    tmp_poses = poses
                if terms == tmp_poses:
                    yield (tokens, poses) if\
                            not include_values else\
                            ((tokens, poses), freq)
        else:
            for (tokens, poses), freq in default_dict.items():
                if self.ngram > 1:
                    tmp_tokens = tokens[:self.ngram-1]
                else:
                    tmp_tokens = tokens
                if terms == tmp_tokens:
                    yield (tokens, poses) if\
                            not include_values else\
                            ((tokens, poses), freq)

    def freq_counts(
            self,
            filename,
            size=None,
        ):

        self.ngram_dict = FreqDist()
        with open(
                filename,
                encoding="utf-8",
                errors="ignore"
            ) as fptr:

            lines = fptr.readlines(size)

        for line in lines:
            self.__sentence = line.lower()

            # Counting Step
            self.ngram_dict.update(self.__phi1())

    def freq2prob(
            self,
            include_token=True
        ):
        # need to improve !!!!!!!!!
        ngram_probs = FreqDist()

        if include_token:
            for elem in self.ngram_dict:
                ngram_probs.update(
                    {elem : self.ngram_dict.freq(elem)}
                )
        else:
            new_ngram_dict = FreqDist()
            for elem in self.ngram_dict:
                new_ngram_dict.update(
                    {elem[1]}
                )

            for elem in new_ngram_dict:
                ngram_probs.update(
                    {elem:new_ngram_dict.freq(elem)}
                )

        return ngram_probs

    @property
    # create a list of token with its POS
    def __tokens_pos(self):
        sent = self.__sentence.lower()
        tokens = word_tokenize(sent)
        return pos_tag(tokens)

    @property
    def __ngram_tokens_pos(self):
        # this returns the tuples of token pos pair
        return ngrams(
            self.__tokens_pos,
            self.ngram
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
