from nltk import *
from math import inf


class PosNgram():

    def __init__(self, context="", ngram=1):
        self.ngram = ngram

        # normalizing the context is very important!!
        self.__sentence = context.lower()

    def __ngram_tokens_pos(self):
        # this returns the tuples of token pos pair
        return ngrams(
            self.__tokens_pos,
            self.ngram
        )

    def tuples_of_token_pos(self, word):
        # normalizing the word is very important!!
        word = word.lower()
        if word not in self.__sentence:
            return []

        for ngram in ngrams(self.__tokens_pos, self.ngram):
            # check if word is included in the ngram

            term_is_in_ngram = any([
                True if word in item else False
                for item in ngram])

            if term_is_in_ngram:
                yield ngram

    def phi1(self, include_token=False):
        """
        This function maps terms to POS
        """
        for elems in self.__ngram_tokens_pos():
            poses = [elem[1] for elem in elems]

            if include_token:
                tokens = [elem[0] for elem in elems]
                yield (tuple(tokens), tuple(poses))
            else:
                yield tuple(poses)

    @property
    # create a list of token with its POS
    def __tokens_pos(self):
        sent = self.__sentence.lower()
        tokens = word_tokenize(sent)
        return pos_tag(tokens)

def terms2poses(terms, ngram_dict):
    pass


def freq_count(filename, ngram=1, size=None):
    ngram_dict = FreqDist()

    with open(filename, encoding="utf-8", errors="ignore") as fptr:
        lines = fptr.readlines(size)

    for line in lines:
        model = PosNgram(line, ngram)

        # Counting
        ngram_dict += FreqDist(model.phi1())

    return ngram_dict


def predict_next_words(ngram_sent, ngram_prob, word_nums=1):
    next_words = []
    return new_words


def freq_count2prob(ngram_dict):
    total_tokens = len(ngram_dict)

    new_dict = {
        token: freq / total_tokens
        for token, freq in ngram_dict.items()
    }
    return new_dict


def argmax_pos(poses):
    max_token, max_freq = tuple(), -inf

    for token, freq in poses:
        max_token = token
        max_freq = max(freq, max_freq)

    return (max_token, max_freq)


if __name__ == '__main__':
    # testing

    filename = "conversation_sample.txt"
    # filename = "gutenberg.txt"; size = 10**5

    u_freq = freq_count(filename)
    u_prob = freq_count2prob(u_freq)

    b_freq = freq_count(filename, 2)
    b_prob = freq_count2prob(b_freq)

    t_freq = freq_count(filename, 2)
    t_prob = freq_count2prob(t_freq)
