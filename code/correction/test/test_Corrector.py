# L. Amber Wilcox-O'Hearn 2013
# test_Corrector.py

from code.correction import Corrector
import unittest


class BeamTest(unittest.TestCase):

    def test_beam_search(self):

        def probability_of_error_function(tokens):
            return 0.01
        def variation_generator(tokens):
            token = tokens[-1]
            if len(token) > 2:
                return []
            else:
                return [ tokens[:-1] + [var] for var in  [token + x for x in 'abcde'] ]
        def path_probability_function(previous_prob, tokens):
            num_a_s = tokens[-1].count('a')
            if len(tokens) > 3 and tokens[1] == 'isd':
                return previous_prob + 1 + .9 ** (len(tokens[-1]) - num_a_s) * .999999 ** num_a_s
            return previous_prob + .9 ** (len(tokens[-1]) - num_a_s) * .999999 ** num_a_s

        width = 5
        sentence = ['This', 'is', 'a', 'bad', 'sentence', '.']
        best_sentence = Corrector.beam_search(sentence, width, probability_of_error_function, path_probability_function, variation_generator)
        self.assertListEqual(best_sentence, ['This', 'isa', 'aa', 'bad', 'sentence', '.a'])

        width = 50
        best_sentence = Corrector.beam_search(sentence, width, probability_of_error_function, path_probability_function, variation_generator)
        self.assertListEqual(best_sentence, ['This', 'isd', 'aa', 'bad', 'sentence', '.a'])

        sentence = ['This', 'isn\'t', 'bad', '...']
        best_sentence = Corrector.beam_search(sentence, width, probability_of_error_function, path_probability_function, variation_generator)
        self.assertListEqual(best_sentence, ['This', 'isn\'t', 'bad', '...'])


if __name__ == '__main__':
    unittest.main()
