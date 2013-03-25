# L. Amber Wilcox-O'Hearn 2013
# Corrector.py

class SentencePath:
    """
    This recursive structure represents a partial sentence.  It
    consists of the SentencePath it was derived from (prior), the new
    word that was added to that prior, and the new total log
    probability associated with the partial sentence.
    """
    def __init__(self, word, prob, prior):
        self.word = word
        self.prob = prob
        self.prior = prior
    def __cmp__(self, other):
        return cmp(self.prob, other.prob)
    def tokens(self):
        tokens = [self.word]
        p = self.prior
        while p:
            tokens.append(p.word)
            p = p.prior
        tokens.reverse()
        return tokens
    def __repr__(self):
        path_tuple_list = [(self.word, self.prob)]
        p = self.prior
        while p:
            path_tuple_list.append((p.word, p.prob))
            p = p.prior
        path_tuple_list.reverse()
        return '<%s %s>' % (self.__class__.__name__, repr(path_tuple_list))

