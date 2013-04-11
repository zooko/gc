# L. Amber Wilcox-O'Hearn 2013
# Corrector.py

def beam_search(sentence, width, prob_of_err_func, path_prob_func, variation_generator):
    """
    For each token in the sentence, put all variations on every
    existing path on the beam.  Sort and prune. At the end, return the
    best path.
    A path is just a tuple of a log probability and a list of tokens.
    """

    beam = [(0, [])]
    for i in range(len(sentence)):
        new_beam = []
        for path in beam:
            path_log_prob, path_tokens = path
            path_with_next_original_token = path_tokens + [sentence[i]]
            new_beam.append( (path_log_prob + path_prob_func(path_with_next_original_token), path_with_next_original_token) )
            for path_variation in variation_generator(path_with_next_original_token):
                new_beam.append( (path_log_prob + path_prob_func(path_variation) + prob_of_err_func(path_variation), path_variation) )

        new_beam.sort()
        beam = new_beam[-width:]

    return beam[-1][1]
