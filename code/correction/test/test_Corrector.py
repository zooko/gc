# L. Amber Wilcox-O'Hearn 2013
# test_Corrector.py

from code.correction import Corrector, VariationProposer
from code.preprocessing import StanfordTaggerPipe
from BackOffTrigramModel import BackOffTrigramModelPipe
import unittest, json

def probability_of_error_function():
    return 0.01
def variation_generator(sentence):
    tokens = sentence.split()
    token = tokens[-1]
    if len(token) > 2:
        return [ ]
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

stanford_tagger_path = 'stanford-tagger/stanford-postagger.jar:'
module_path = 'edu.stanford.nlp.tagger.maxent.MaxentTagger'
model_path = 'stanford-tagger/english-left3words-distsim.tagger'

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

    def test_trigram_path_probability(self):

        tmpipe_obj = BackOffTrigramModelPipe.BackOffTMPipe('BackOffTrigramModelPipe', 'code/correction/test/trigram_model_5K.arpa')
        tagger_pipe = StanfordTaggerPipe.StanfordTaggerPipe(stanford_tagger_path, module_path, model_path)
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        small_insertables = json.load(open('code/correction/test/small_insertables', 'r'))
        small_deletables = json.load(open('code/correction/test/small_deletables', 'r'))
        var_gen = VariationProposer.VariationProposer(tagger_pipe.tags_list, pos_dictionary, tmpipe_obj, small_insertables, small_deletables)
        corrector = Corrector.Corrector(tmpipe_obj, 25, var_gen.generate_path_variations, -1.3)

        tokens = u'The I over'.split()
        tpp = corrector.trigram_path_probability(tokens)
        self.assertAlmostEqual(tpp, -4.185007, msg=tpp)

    def test_get_correction(self):
        '''
        This is a regression test and a test of pieces working
        together, not of the correctness of results.
        '''

        tmpipe_obj = BackOffTrigramModelPipe.BackOffTMPipe('BackOffTrigramModelPipe', 'code/correction/test/trigram_model_5K.arpa')
        tagger_pipe = StanfordTaggerPipe.StanfordTaggerPipe(stanford_tagger_path, module_path, model_path)
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        small_insertables = json.load(open('code/correction/test/small_insertables', 'r'))
        small_deletables = json.load(open('code/correction/test/small_deletables', 'r'))
        var_gen = VariationProposer.VariationProposer(tagger_pipe.tags_list, pos_dictionary, tmpipe_obj, small_insertables, small_deletables)
        corrector = Corrector.Corrector(tmpipe_obj, 5, var_gen.generate_path_variations, -1.3)

        tokens = "This will , if not already , caused problems as there are very limited spaces for us .".split()
        result = corrector.get_correction(tokens)
        self.assertListEqual(result, [u'This', u'will', u',', u'if', u'not', u'have', u'already', u'been', u',', u'has', u'caused', u'the', u'problems', u'as', u'there', u'are', u'very', u'limited', 'space', 'for', 'us', '.'], result)
        tokens = u"I agree to a large extent that current policies have helped to ease the aging process .".split()
        result = corrector.get_correction(tokens)
        self.assertListEqual(result, [u'I', u'agree', u'to', u'a', u'large', u'extent', u'that', u'current', u'policies', u'have', u'helped', u'to', u'ease', u'the', u'aging', u'process', u'.'] , result)

    def test_pos_correction(self):
        pass

        tmpipe_obj = BackOffTrigramModelPipe.BackOffTMPipe('BackOffTrigramModelPipe', 'code/correction/test/pos_trigram_model_0.1K.arpa')
        tagger_pipe = StanfordTaggerPipe.StanfordTaggerPipe(stanford_tagger_path, module_path, model_path)
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        small_insertables = json.load(open('code/correction/test/small_insertables', 'r'))
        small_deletables = json.load(open('code/correction/test/small_deletables', 'r'))
        var_gen = VariationProposer.VariationProposer(tagger_pipe.tags_list, pos_dictionary, tmpipe_obj, small_insertables, small_deletables)
        corrector = Corrector.Corrector(tmpipe_obj, 5, var_gen.generate_path_variations, -1.3, pos=True, tagger=tagger_pipe.tags_list)

        tokens = u'The dogs is black'.split()
        best_tokens = corrector.get_correction(tokens)
        self.assertListEqual(best_tokens, [u'The', u'dogs', u'is', u'black'], best_tokens)

        tokens = u'I am walked home'.split()
        best_tokens = corrector.get_correction(tokens)
        self.assertListEqual(best_tokens, [u'Be', u'I', u'to', u'am', u'the', u'walked', u'home'], best_tokens)


if __name__ == '__main__':
    unittest.main()
