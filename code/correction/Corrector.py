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

            path_avg_word_log_prob, path_tokens = path
            total_log_prob = path_avg_word_log_prob * len(path_tokens)

            path_with_next_original_token = path_tokens + [tokens[i]]
#            print "Here I am with next token:", path_with_next_original_token

            next_word_prob = path_prob_func(path_with_next_original_token)
#            print "Here's my next_word_prob:", next_word_prob

            avg_word_prob = (total_log_prob + next_word_prob) / len(path_with_next_original_token)
#            print "Here's my new avg-word prob:", avg_word_prob

            new_beam.append( (avg_word_prob, path_with_next_original_token) )

            token_string = ' '.join(path_with_next_original_token)
            for path_variation in variation_generator(token_string):
                assert(path_variation != path_with_next_original_token)
#                print "I'm a variation:", path_variation

                # If we had a deletion:
                if path_variation == path_tokens:

                    # If this was not the first word:
                    if len(path_variation) > 0:
                        avg_word_prob = (total_log_prob + prob_of_err_func()) / len(path_variation)
#                        print "Here's my new avg-word prob:", avg_word_prob

                    # If this was the first word:
                    else:
                        avg_word_prob = 0
#                        print "Here's my new avg-word prob:", avg_word_prob

                # If we had an insertion
                elif len(path_variation) > len(path_tokens) + 1:
                    insertion_prob = path_prob_func(path_variation[:-1])
#                    print "Here's the prob of my insertion: ", insertion_prob

                    next_word_prob = path_prob_func(path_variation)
#                    print "And here's my next word prob:", next_word_prob

#                    print "Original: ", tokens[i], "last in variation: ", path_variation[-1]
                    # If the last word is the original:
                    if path_variation[-1] == tokens[i]:
#                        print "Last word was original."
                        number_of_errors = 1
                    else:
                        number_of_errors = 2

                    avg_word_prob = (total_log_prob + insertion_prob + next_word_prob + number_of_errors * prob_of_err_func()) / len(path_variation)
#                    print "Here's my per-word prob:", avg_word_prob

                # If there was no deletion or insertion, but a substitution
                else:
                    next_word_prob = path_prob_func(path_variation)
#                    print "And here's my next_word_prob:", next_word_prob

                    avg_word_prob = (total_log_prob + next_word_prob + prob_of_err_func()) / len(path_variation)
#                    print "Here's my per-word prob:", avg_word_prob

                new_beam.append( (avg_word_prob, path_variation) )

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
           word = path[0].lower()
           return self.trigram_model_pipe.trigram_probability(['<s>', '<s>', word])
       if len(path) == 2:
           word1 = path[0].lower()
           word2 = path[1].lower()
           return self.trigram_model_pipe.trigram_probability(['<s>', word1, word2])
       else:
           word1 = path[-3].lower()
           word2 = path[-2].lower()
           word3 = path[-1].lower()
           return self.trigram_model_pipe.trigram_probability([word1, word2, word2])


    def get_correction(self, tokens):

        return beam_search(tokens, self.width, self.get_error_prob, self.trigram_path_probability, self.variation_generator)
