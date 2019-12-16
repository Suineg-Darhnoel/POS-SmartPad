from math import log
from math import exp
from nltk import ngrams, pos_tag, word_tokenize, FreqDist
from progress.bar import IncrementalBar as ICB


class PosNgram:

    def __init__(self, deg=1):
        self.order = deg
        self.__sentence = ""

        # storing tokens and frequency
        self.ngram_data = FreqDist()

        # to prevent from illegral argument
        if deg < 1:
            self.order = 1

    def poses_data(self):
        tmp_data = FreqDist()
        for (_, pos), freq in self.ngram_data.items():
            tmp_data.update({pos:freq})
        return tmp_data

    def tokens_data(self):
        tmp_data = FreqDist()
        for (token, _), freq in self.ngram_data.items():
            tmp_data.update({token:freq})
        return tmp_data

    def poses2tokens(
            self,
            pos_terms,
            include_freq=False,
            default_dict=None
        ):
        """
        # The token_terms must be the element of ngram_model
        # whose order is 1 smaller than that of the current one.
        """
        if default_dict is None:
            default_dict = self.ngram_data

        for (tokens, poses), freq in default_dict.items():
            if pos_terms == poses:
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
        # whose order is 1 smaller than that of the current one.
        """
        if default_dict is None:
            default_dict = self.ngram_data

        for (tokens, poses), freq in default_dict.items():
            if token_terms == tokens:
                yield poses if\
                        not include_freq\
                        else (poses, freq)

    def pre_process(
            self,
            *filenames,
            size=None,
        ):

        self.ngram_data = FreqDist()
        for filename in filenames:
            with open(
                    filename,
                    encoding="utf-8",
                    errors="ignore"
                ) as fptr:

                lines = fptr.readlines(size)

            line_nums = len(lines)
            print(filename, "ngram's order={}".format(self.order))
            with ICB('Processing...', max=line_nums) as bar:
                for line in lines:
                    bar.next()
                    self.__sentence = line.lower()

                    # Counting Step
                    self.ngram_data.update(self.__token_pos_pairs)

        print('dict_size = {}'.format(self.ngram_data.B()))

    def __freq2prob(
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

    def freq_count(self, term, target='pos'):
        tmp_freq = 0
        if target == 'pos':
            for (_, p), freq in self.ngram_data.items():
                if term == p:
                    # print(_, p, freq)
                    tmp_freq += freq
        else:
            for (t, _), freq in self.ngram_data.items():
                if term == t:
                    # print(t, _, freq)
                    tmp_freq += freq

        return tmp_freq

    def __is_subcontent(self, w1, w2):
        assert len(w1) <= len(w2)
        w1 = list(w1)
        w2 = list(w2)
        for w in w1:
            if w not in w2:
                return False
            w2.remove(w)
        return True

    def fetch_if_prefix(self, term, fetch_target='pos'):
        tmp_set = FreqDist()
        if fetch_target == 'pos':
            for (token, pos), freq in self.ngram_data.items():
                curr_pos = pos[:-1]
                if curr_pos == term:
                    tmp_set.update({pos: freq})
        else:
            for (token, pos), freq in self.ngram_data.items():
                curr_token = token[:-1]
                if curr_token == term:
                    tmp_set.update({token: freq})
        return tmp_set

    def fetch_if_suffix(self, term, fetch_target='pos'):
        tmp_set = FreqDist()
        if fetch_target == 'pos':
            for (token, pos), freq in self.ngram_data.items():
                curr_pos = pos[-len(term):]
                if curr_pos == term:
                    tmp_set.update({pos: freq})
        else:
            for (token, pos), freq in self.ngram_data.items():
                curr_token = token[-len(term):]
                if curr_token == term:
                    tmp_set.update({token: freq})
        return tmp_set

    def fetch_if_contain(self, term, fetch_target='pos'):
        tmp_set = FreqDist()
        if fetch_target == 'pos':
            for (token, pos), freq in self.ngram_data.items():
                if self.__is_subcontent(term, pos):
                    tmp_set.update({pos: freq})
        else:
            for (token, pos), freq in self.ngram_data.items():
                if self.__is_subcontent(term, token):
                    tmp_set.update({token: freq})
        return tmp_set

    def show_prob_info(self, mc=10, include_token=False):
        for elem in self.__freq2prob(include_token).most_common(mc):
            print(elem)

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
            self.order
        )


if __name__ == '__main__':
    # testing
    filenames = [
        "data/austen-emma.txt",
        "data/science.txt"
    ]
    size = 10**5 # just 1/8 of the whole file
    # size = None

    u_model = PosNgram(1)
    b_model = PosNgram(2)
    t_model = PosNgram(3)

    u_model.pre_process(*filenames, size=size)
    b_model.pre_process(*filenames, size=size)
    t_model.pre_process(*filenames, size=size)
