# L. Amber Wilcox-O'Hearn 2013
# Corrector.py

def beam_search(tagged_tokens, width, prob_of_err, path_prob_func, variation_generator, verbose=False):
    """
    tagged_tokens is a list of tuples of tokens and tags.
    For each tuple in tagged_tokens, put all variations on every
    existing path on the beam.  Sort and prune. At the end, return the
    best path.
    A path is just a tuple of a log probability and a list of (token, tag) tuples.
    The log probability is a per word probability.
    """

    beam = [(0, [])]
    for i in range(len(tagged_tokens)):
        new_beam = []
        for path in beam:
            if verbose:
                print "I'm a path in the beam:", path

            path_avg_word_log_prob, path_tuples = path
            total_log_prob = path_avg_word_log_prob * len(path_tuples)

            path_with_next_original_token = path_tuples + [tagged_tokens[i]]
            if verbose:
                print "Here I am with next token:", path_with_next_original_token

            next_word_prob = path_prob_func(path_with_next_original_token)
            if verbose:
                print "Here's my next_word_prob:", next_word_prob

            avg_word_prob = (total_log_prob + next_word_prob) / len(path_with_next_original_token)
            if verbose:
                print "Here's my new avg-word prob:", avg_word_prob

            new_beam.append( (avg_word_prob, path_with_next_original_token) )

            for path_variation in variation_generator(path_with_next_original_token):
                assert path_variation != path_with_next_original_token, path_variation
                if verbose:
                    print "I'm a variation:", path_variation

                # If we had a deletion:
                if path_variation == path_tuples:

                    # If this was not the first word:
                    if len(path_variation) > 0:
                        avg_word_prob = (total_log_prob + prob_of_err) / len(path_variation)
                        if verbose:
                            print "Here's my new avg-word prob:", avg_word_prob

                    # If this was the first word:
                    else:
                        avg_word_prob = 0
                        if verbose:
                            print "Here's my new avg-word prob:", avg_word_prob

                # If we had an insertion
                elif len(path_variation) > len(path_tuples) + 1:
                    insertion_prob = path_prob_func(path_variation[:-1])
                    if verbose:
                        print "Here's the prob of my insertion: ", insertion_prob

                    next_word_prob = path_prob_func(path_variation)
                    if verbose:
                        print "And here's my next word prob:", next_word_prob

                    # If the last word is the original:
                    if path_variation[-1] == tagged_tokens[i]:
                        number_of_errors = 1
                    else:
                        number_of_errors = 2

                    avg_word_prob = (total_log_prob + insertion_prob + next_word_prob + number_of_errors * prob_of_err) / len(path_variation)
                    if verbose:
                        print "Here's my per-word prob:", avg_word_prob

                # If there was no deletion or insertion, but a substitution
                else:
                    next_word_prob = path_prob_func(path_variation)
                    if verbose:
                        print "And here's my next_word_prob:", next_word_prob

                    avg_word_prob = (total_log_prob + next_word_prob + prob_of_err) / len(path_variation)
                    if verbose:
                        print "Here's my per-word prob:", avg_word_prob

                new_beam.append( (avg_word_prob, path_variation) )

        new_beam.sort()
        beam = new_beam[-width:]
        if verbose:
            print "I am a beam:", beam, '\n'

    return beam[-1][1]

class Corrector():

    def __init__(self, trigram_model_pipe, width, variation_generator, error_prob, verbose=False, pos=0, pos_ngram_server_obj=None, closed_class=0, closed_class_pos_ngram_server_obj=None, closed_class_tags=None, AUX=None):

        self.trigram_model_pipe = trigram_model_pipe
        self.width = width
        self.variation_generator = variation_generator
        self.error_prob = error_prob
        self.verbose = verbose
        self.pos = pos
        self.pos_ngram_server_obj = pos_ngram_server_obj
        self.closed_class = closed_class
        self.closed_class_pos_ngram_server_obj = closed_class_pos_ngram_server_obj
        self.closed_class_tags = closed_class_tags
        self.AUX = AUX

    def ngram_path_probability(self, path, pipe='t'):
       '''
       path is a list of tuples with at least one element.
       pipe can be 't' for trigram, 'p' for pos, or 'c' for closed_class
       '''

       if pipe == 't':
           tokens = ['<s>', '<s>'] + [w.lower() for w in path[-3:]]
           word1, word2, word3 = tokens[-3:]

           if self.verbose:
               print "Submitting to trigram model:", word1, word2, word3

           result = self.trigram_model_pipe.trigram_probability([word1, word2, word3])

           if self.verbose:
               print "And got:", result

           return result

       elif pipe == 'p':
           tokens = 4*['<s>'] + [w for w in path[-5:]]
           word1, word2, word3, word4, word5 = tokens[-5:]

           if self.verbose:
               print "Submitting to ngram model:", word1, word2, word3, word4, word5

           result = self.pos_ngram_server_obj.log_probability([word1, word2, word3, word4, word5])
           if self.verbose:
               print "And got:", result

           return result

       elif pipe == 'c':
           tokens = 4*['<s>'] + [w for w in path[-5:]]
           word1, word2, word3, word4, word5 = tokens[-5:]

           if self.verbose:
               print "Submitting to ngram model:", word1, word2, word3, word4, word5

           result = self.closed_class_pos_ngram_server_obj.log_probability([word1, word2, word3, word4, word5])

           if self.verbose:
               print "And got:", result

           return result

       else:
           assert False, "pipe must be one of 't', 'p', or 'c'"


    def pos_ngram_path_probability(self, path):

        if self.pos:
            tags = [p[1] for p in path]
            pos_prob = self.ngram_path_probability(tags, pipe='p')
        else:
            pos_prob = 0
        if self.pos == 1:
            return pos_prob

        return self.pos * pos_prob + (1-self.pos) * self.ngram_path_probability([p[0] for p in path])

    def closed_class_pos_ngram_path_probability(self, path):

        if self.closed_class:
            closed_class_path = [p[0].lower() if (p[1] in self.closed_class_tags or p[0] in self.AUX) else p[1] for p in path]
            closed_class_prob = self.ngram_path_probability(closed_class_path, pipe='c')
            assert isinstance(closed_class_prob, (int, float, long)), "%r :: %s -- closed_class_path: %s" % (closed_class_prob, type(closed_class_prob), closed_class_path)
        else:
            closed_class_prob = 0

        if self.closed_class == 1:
            return closed_class_prob

        assert isinstance(self.closed_class, (int, float, long)), "%r :: %s" % (self.closed_class, type(self.closed_class))
        assert isinstance(closed_class_prob, (int, float, long)), "%r :: %s" % (closed_class_prob, type(closed_class_prob))

        x = self.ngram_path_probability([p[0] for p in path])
        assert isinstance(x, (int, float, long)), "%r :: %s" % (x, type(x))

        return self.closed_class * closed_class_prob + (1-self.closed_class) * x

    def get_correction(self, tokens):

        if self.closed_class:
            assert not self.pos, "POS and closed class models can't both be set."
            return beam_search(tokens, self.width, self.error_prob, self.closed_class_pos_ngram_path_probability, self.variation_generator, self.verbose)

        return beam_search(tokens, self.width, self.error_prob, self.pos_ngram_path_probability, self.variation_generator, self.verbose)

