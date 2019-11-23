from nltk import *

with open("conversation_sample.txt") as fptr:
    lines = fptr.readlines()

class PosNgram:

    def __init__(self, ngram=1, sentence=""):
        self.ngram = ngram
        self.__sentence = sentence

    def phi_apo(self):
        """
        This function maps terms to POS
        """
        return set(ngrams(
                self.__tokens_pos,
                self.ngram
            )
        )

    def phi_double_apo(self, word):
        """
        This function is important for computing a term weight
        from POS n-grams, because it maps a term to all the POS
        n-grams that 'contain' it.
        """
        word = word.lower()
        result = []

        if word not in self.__sentence:
            return result

        for ngram in ngrams(self.__tokens_pos, self.ngram):
            # check if word is included in the ngram

            term_is_in_ngram = any([
                True if word in item else False
                for item in ngram])

            if term_is_in_ngram:
                result.append(ngram)

        return set(result)

    @property
    # create a list of token with its POS
    def __tokens_pos(self):
        sent = self.__sentence.lower()
        tokens = word_tokenize(sent)
        return pos_tag(tokens)

sentence = "The cat sat on the mat"
ug = PosNgram(1, sentence)
bg = PosNgram(2, sentence)
tr = PosNgram(3, sentence)
