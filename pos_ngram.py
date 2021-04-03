from math import log
from math import exp
from math import floor
from nltk import ngrams, pos_tag, word_tokenize, FreqDist
from nltk.corpus import gutenberg
from progress.bar import IncrementalBar as ICB
from past.builtins import execfile
import time

# GLOBAL VARIABLE
ng_suffix = 'suffix'
ng_prefix = 'prefix'
ng_contain = 'contain'
ng_equal = 'equal'

class PosNgram:

    def __init__(self, deg=1):
        self.order = deg
        self.__sentence = ""

        # storing tokens and frequency
        self.train_data = FreqDist()
        self.test_sents = None

        # to prevent from illegral argument
        if deg < 1:
            self.order = 1

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
            default_dict = self.train_data

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
            default_dict = self.train_data

        for (tokens, poses), freq in default_dict.items():
            if token_terms == tokens:
                yield poses if\
                        not include_freq\
                        else (poses, freq)

    def pre_process(
            self,
            file_id,
            training_size=90
        ):

        start_processing = time.time()
        self.train_data = FreqDist()

        sents = gutenberg.sents(file_id)
        t_size = floor((training_size/100) * len(sents))

        train_sents = sents[:t_size]
        self.test_sents = sents[t_size:]

        p_title = "file_id = <{}>, ngram's order = {}, split_ratio = {}-{}"
        print(p_title.format(
                file_id,
                self.order,
                training_size,
                100-training_size)
            )
        with ICB(
                    'Processing...',
                    max=len(train_sents),
                    suffix='%(percent)d%%'
                ) as bar:

            for sent in train_sents:
                bar.next()
                self.__sentence = " ".join(sent)
                self.train_data.update(self._token_pos_pairs)

        print('dict_size = {}'.format(self.train_data.B()))
        print("loading time = {}".format(time.time()-start_processing))

    def _is_subcontent(self, w1, w2):
        assert len(w1) <= len(w2)
        w1 = list(w1)
        w2 = list(w2)
        for w in w1:
            if w not in w2:
                return False
            w2.remove(w)
        return True

    def fetch_if(
            self,
            cond,
            term,
            pos_is_target=True,
            include_pair=False
        ):

        tmp_freq_dist = FreqDist()

        conditions = {
            ng_prefix : [
                "pos[:-1] == term",
                "token[:-1] == term"
            ],
            ng_suffix : [
                "pos[-len(term):] == term",
                "token[-len(term):] == term"
            ],
            ng_contain : [
                "self._is_subcontent(term, pos)",
                "self._is_subcontent(term , token)"
            ],
            ng_equal: [
                "pos == term",
                "token == term"
            ]
        }

        if cond not in conditions:
            cond = prefix

        # Fetching Choice Configuration
        p_key, t_key = "", ""
        if include_pair:
            p_key = "(pos, token)"
            t_key = "(token, pos)"
        else:
            p_key = "pos"
            t_key = "token"
        cmp_p = compile(p_key, '<string>', 'eval')
        cmp_t = compile(t_key, '<string>', 'eval')

        if pos_is_target:
            cmp_cond = compile(
                    conditions[cond][0],
                    '<string>',
                    'eval'
                )
            for (token, pos), freq in self.train_data.items():
                if eval(cmp_cond):
                    tmp_freq_dist.update({eval(cmp_p): freq})
        else:
            cmp_cond = compile(
                    conditions[cond][1],
                    '<string>',
                    'eval'
                )
            for (token, pos), freq in self.train_data.items():
                if eval(cmp_cond):
                    tmp_freq_dist.update({eval(cmp_t): freq})

        return tmp_freq_dist

    @property
    def _token_pos_pairs(self):
        """
        This function maps terms to POS
        (The previous version's name was phi1)
        """
        for elems in self._ngram_tokens_pos:
            poses = [elem[1] for elem in elems]

            tokens = [elem[0] for elem in elems]
            yield (tuple(tokens), tuple(poses))

    @property
    def _sent2pos_tag(self):
        sent = self.__sentence
        tokens = word_tokenize(sent)
        return pos_tag(tokens)

    @property
    def _ngram_tokens_pos(self):
        # this returns the tuples of token pos pair
        return ngrams(
            self._sent2pos_tag,
            self.order
        )


if __name__ == '__main__':
    execfile('Mytest.py')
