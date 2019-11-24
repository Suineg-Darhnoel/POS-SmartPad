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

    def phi2(self, word, include_token=False):
        """
        This function is important for computing a term weight
        from POS n-grams, because it maps a term to all the POS
        n-grams that 'contain' it.
        """
        for tples in self.tuples_of_token_pos(word):
            tmp_tokens, tmp_poses = [], []

            for token, pos in tples:
                tmp_tokens.append(token)
                tmp_poses.append(pos)

            if include_token:
                yield (tuple(tmp_tokens), tuple(tmp_poses))
            else:
                yield tuple(tmp_poses)

    @property
    # create a list of token with its POS
    def __tokens_pos(self):
        sent = self.__sentence.lower()
        tokens = word_tokenize(sent)
        return pos_tag(tokens)


def ngram_probs(poses):
    elem_nums = len(poses)

    for token, freq in poses.items():
        yield (token, freq / elem_nums)


def argmax_pos(poses):
    max_token, max_freq = tuple(), -inf

    for token, freq in poses:
        max_token = token
        max_freq = max(freq, max_freq)

    return (max_token, max_freq)


if __name__ == '__main__':
    # testing

    with open("conversation_sample.txt", errors='ignore') as fptr:
        lines = fptr.readlines()

    ngram_dict1 = FreqDist()
    for line in lines:
        ngram_model1 = PosNgram(line, 2)

        # start counting
        ngram_dict1 += FreqDist(
                    ngram_model1.phi2("have", include_token=False)
                )

    for elem in ngram_dict1.items():
        print(elem)
    print(len(ngram_dict1))
