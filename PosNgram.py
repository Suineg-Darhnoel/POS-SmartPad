from math import log
from math import exp
from nltk import ngrams, pos_tag, word_tokenize, FreqDist
from progress.bar import IncrementalBar as ICB
from past.builtins import execfile

# GLOBAL VARIABLE
ng_suffix = 'suffix'
ng_prefix = 'prefix'
ng_contain = 'contain'

class PosNgram:

    def __init__(self, deg=1):
        self.order = deg
        self.__sentence = ""

        # storing tokens and frequency
        self.ngram_data = FreqDist()

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
                    self.ngram_data.update(self._token_pos_pairs)

        print('dict_size = {}'.format(self.ngram_data.B()))

    def _freq2prob(
            self,
            include_token=True
        ):
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
            for (token, pos), freq in self.ngram_data.items():
                if eval(cmp_cond):
                    tmp_freq_dist.update({eval(cmp_p): freq})
        else:
            cmp_cond = compile(
                    conditions[cond][1],
                    '<string>',
                    'eval'
                )
            for (token, pos), freq in self.ngram_data.items():
                if eval(cmp_cond):
                    tmp_freq_dist.update({eval(cmp_t): freq})

        return tmp_freq_dist

    def show_prob_info(self, mc=10, include_token=False):
        for elem in self._freq2prob(include_token).most_common(mc):
            print(elem)

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
        sent = self.__sentence.lower()
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
