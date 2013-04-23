# L. Amber Wilcox-O'Hearn 2013
# Corrector.py

def beam_search(tagged_tokens, width, prob_of_err_func, path_prob_func, variation_generator, verbose=False):
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
                        avg_word_prob = (total_log_prob + prob_of_err_func()) / len(path_variation)
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

                    avg_word_prob = (total_log_prob + insertion_prob + next_word_prob + number_of_errors * prob_of_err_func()) / len(path_variation)
                    if verbose:
                        print "Here's my per-word prob:", avg_word_prob

                # If there was no deletion or insertion, but a substitution
                else:
                    next_word_prob = path_prob_func(path_variation)
                    if verbose:
                        print "And here's my next_word_prob:", next_word_prob

                    avg_word_prob = (total_log_prob + next_word_prob + prob_of_err_func()) / len(path_variation)
                    if verbose:
                        print "Here's my per-word prob:", avg_word_prob

                new_beam.append( (avg_word_prob, path_variation) )

        new_beam.sort()
        beam = new_beam[-width:]
        if verbose:
            print "I am a beam:", beam, '\n'

    return beam[-1][1]

class Corrector():

    def __init__(self, trigram_model_pipe, width, variation_generator, error_prob, verbose=False, pos=0, pos_tmpipe_obj=None):

        self.trigram_model_pipe = trigram_model_pipe
        self.width = width
        self.variation_generator = variation_generator
        self.error_prob = error_prob
        self.verbose = verbose
        self.pos = pos
        self.pos_tmpipe_obj = pos_tmpipe_obj

    def get_error_prob(self):
       return self.error_prob

    def trigram_path_probability(self, path, pipe='t', lower=True):
       '''
       path is a list of tuples with at least one element.
       '''

       if lower:
           tokens = ['<s>', '<s>'] + [w.lower() for w in path[-3:]]
       else:
           tokens = ['<s>', '<s>'] + [w for w in path[-3:]]
       word1, word2, word3 = tokens[-3:]

       if self.verbose:
           print "Submitting to trigram model:", word1, word2, word3

       if pipe == 't':
           return self.trigram_model_pipe.trigram_probability([word1, word2, word3])
       elif pipe == 'p':
           return self.pos_tmpipe_obj.trigram_probability([word1, word2, word3])


    def pos_trigram_path_probability(self, path):

        if self.pos:
            tags = [p[1] for p in path]
            pos_prob = self.trigram_path_probability(tags, pipe='p', lower=False)
        else:
            pos_prob = 0
        if self.pos == 1:
            return pos_prob

        return self.pos * pos_prob + (1-self.pos) * self.trigram_path_probability([p[0] for p in path])

    def get_correction(self, tokens):

        return beam_search(tokens, self.width, self.get_error_prob, self.pos_trigram_path_probability, self.variation_generator, self.verbose)

