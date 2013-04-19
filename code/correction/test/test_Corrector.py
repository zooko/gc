# L. Amber Wilcox-O'Hearn 2013
# test_Corrector.py

from code.correction import Corrector, VariationProposer
from code.preprocessing import StanfordTaggerPipe
import unittest, json

def probability_of_error_function(tokens):
    return 0.01
def variation_generator(sentence):
    tokens = sentence.split()
    token = tokens[-1]
    if len(token) > 2:
        return [ tokens ]
    else:
        if token == '.':
            return [ tokens[:-1] + [var] for var in  [token + x for x in 'abcde'] ] + [ tokens[:-1] ]
        else:
            return [ tokens[:-1] + [var] for var in  [token + x for x in 'abcde'] ]
def path_probability_function(tokens):
    num_a_s = tokens[-1].count('a')
    num_periods = tokens.count(['.'])
    if len(tokens) > 3 and tokens[1] == 'isd':
        return 1 + .9 ** (len(tokens[-1]) - num_a_s) * .999999 ** num_a_s - len(tokens)
    return .9 ** (len(tokens[-1]) - num_a_s) * .999999 ** num_a_s - len(tokens)

class CorrectorTest(unittest.TestCase):

    def test_beam_search(self):

        tokens = ['This', 'is', 'a', 'bad', 'sentence', '.']

        width = 5
        best_tokens = Corrector.beam_search(tokens, width, probability_of_error_function, path_probability_function, variation_generator)
        self.assertListEqual(best_tokens, ['This', 'isa', 'aa', 'bad', 'sentence'])

        width = 50
        best_tokens = Corrector.beam_search(tokens, width, probability_of_error_function, path_probability_function, variation_generator)
        self.assertListEqual(best_tokens, ['This', 'isd', 'aa', 'bad', 'sentence'])

        tokens = ['This', 'isn\'t', 'bad', '...']
        best_tokens = Corrector.beam_search(tokens, width, probability_of_error_function, path_probability_function, variation_generator)
        self.assertListEqual(best_tokens, ['This', 'isn\'t', 'bad', '...'])

    def test_get_correction(self):
        '''
        This is a regression test and a test of pieces working
        together, not of the correctness of results.
        '''

        from BackOffTrigramModel import BackOffTrigramModelPipe
        tmpipe_obj = BackOffTrigramModelPipe.BackOffTMPipe('BackOffTrigramModelPipe', 'code/correction/test/trigram_model_5K.arpa')
        stanford_tagger_path = 'stanford-tagger/stanford-postagger.jar:'
        module_path = 'edu.stanford.nlp.tagger.maxent.MaxentTagger'
        model_path = 'stanford-tagger/english-left3words-distsim.tagger'
        tagger_pipe = StanfordTaggerPipe.StanfordTaggerPipe(stanford_tagger_path, module_path, model_path)
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        small_insertables = json.load(open('code/correction/test/small_insertables', 'r'))
        small_deletables = json.load(open('code/correction/test/small_deletables', 'r'))
        var_gen = VariationProposer.VariationProposer(tagger_pipe.tags_list, pos_dictionary, tmpipe_obj, small_insertables, small_deletables)
        corrector = Corrector.Corrector(tmpipe_obj, 10, var_gen.generate_path_variations, -3.3)

        tokens = "This will , if not already , caused problems as there are very limited spaces for us .".lower().split()
        result = corrector.get_correction(tokens)
        self.assertListEqual(result, ['this', 'will', ',', 'if', 'not', 'already', ',', 'caused', 'problems', 'as', 'there', 'are', 'very', 'limited', 'spaces', 'for', 'us', '.'], result)

if __name__ == '__main__':
    unittest.main()
