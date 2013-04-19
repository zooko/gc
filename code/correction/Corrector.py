# L. Amber Wilcox-O'Hearn 2013
# Corrector.py


def beam_search(tokens, width, prob_of_err_func, path_prob_func, variation_generator):
    """
    For each token in the tokens, put all variations on every
    existing path on the beam.  Sort and prune. At the end, return the
    best path.
    A path is just a tuple of a log probability and a list of tokens.
    The log probability is a per word probability.
    """

    beam = [(0, [])]
    for i in range(len(tokens)):
        new_beam = []
        for path in beam:
#            print "I'm a path in the beam:", path
            path_log_prob, path_tokens = path
            path_with_next_original_token = path_tokens + [tokens[i]]
#            print "Here I am with next token:", path_with_next_original_token
            prob = path_prob_func(path_with_next_original_token)
#            print "Here's my prob:", prob
            per_word_prob = (path_log_prob * len(path_tokens) + prob) / len(path_with_next_original_token)
            new_beam.append( (per_word_prob, path_with_next_original_token) )
            token_string = ' '.join(path_with_next_original_token)
            for path_variation in variation_generator(token_string):
                assert(path_variation != path_with_next_original_token)
#                print "I'm a variation:", path_variation
                if path_variation == path_tokens: # We had a deletion
                    if len(path_variation) > 0:
                        per_word_prob = (path_log_prob * len(path_tokens) + prob_of_err_func()) / len(path_variation)
                    else:
                        per_word_prob = 0
                elif len(path_variation) > len(path_tokens) + 1: # We had an insertion
                    prob = path_prob_func(path_variation[:-1]) + path_prob_func(path_variation)
#                    print "And here's my prob:", prob
                    if path_variation[-1] == tokens[i]: # var after insertion was original
                        number_of_errors = 1
                    else:
                        number_of_errors = 2
                    per_word_prob = (path_log_prob * len(path_tokens) + prob + number_of_errors * prob_of_err_func()) / len(path_variation)
                else: # No deletion or insertion, and real variation
                    prob = path_prob_func(path_variation)
#                    print "And here's my prob:", prob
                    per_word_prob = (path_log_prob * len(path_tokens) + prob + prob_of_err_func()) / len(path_variation)
                new_beam.append( (per_word_prob, path_variation) )

        new_beam.sort()
        beam = new_beam[-width:]
        print "I am a beam:", beam, '\n'

    return beam[-1][1]

class Corrector():

    def __init__(self, trigram_model_pipe, width, variation_generator, error_prob):

        self.trigram_model_pipe = trigram_model_pipe
        self.width = width
        self.variation_generator = variation_generator
        self.error_prob = error_prob

    def get_error_prob(self):
       return self.error_prob

    def trigram_path_probability(self, path):
       '''
       path is a list of tokens with at least one element.
       '''
       if len(path) == 1:
          return self.trigram_model_pipe.trigram_probability(['<s>', '<s>', path[0]])
       if len(path) == 2:
          return self.trigram_model_pipe.trigram_probability(['<s>', path[0], path[1]])
       else:
          return self.trigram_model_pipe.trigram_probability(path[-3:])


    def get_correction(self, tokens):

        return beam_search(tokens, self.width, self.get_error_prob, self.trigram_path_probability, self.variation_generator)
