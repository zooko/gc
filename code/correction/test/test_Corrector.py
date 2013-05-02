# L. Amber Wilcox-O'Hearn 2013
# test_Corrector.py

from code.language_modelling import SRILMServerPipe
from code.correction import Corrector, VariationProposer
from math import log10
import unittest, json

probability_of_error = log10(0.5)

def variation_generator(tagged_sentence, err_prob):
    tokens = [t[0] for t in tagged_sentence]
    tags = [t[1] for t in tagged_sentence]
    token = tokens[-1]
    if len(token) > 2:
        return [], []
    else:
        if token == '.':
            return [ tagged_sentence[:-1] + [(var, tags[-1])] for var in  [token + x for x in u'abced'] ] + [ tagged_sentence[:-1] ], 4*[probability_of_error] + [3*probability_of_error] + [.001*probability_of_error]
        else:
            return [ tagged_sentence[:-1] + [(var, tags[-1])] for var in  [token + x for x in u'abced'] ], 4*[probability_of_error] + [3*probability_of_error]

def path_probability_function(tagged_tokens):
    '''
    This function penalises sentence length, likes a's, and really
    likes "isd" after a while.
    '''
    tokens = [t[0] for t in tagged_tokens]
    num_a_s = tokens[-1].count(u'a')

    prob = -log10(30*len(tokens))
    if len(tokens) > 3 and tokens[1] == u'isd':
        prob += 1
    if len(tokens) > 5:
        prob -= 1
    return prob + log10(.9) * (5 - num_a_s)

stanford_tagger_path = 'stanford-tagger/stanford-postagger.jar:'
module_path = 'edu.stanford.nlp.tagger.maxent.MaxentTagger'
model_path = 'stanford-tagger/english-left3words-distsim.tagger'
closed_class_tags = ['IN', 'DT', 'TO', 'MD']
AUX = [u'be', u'is', u'are', u'were', u'was', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'get', u'got', u'getting']

BOTMCFFI=True

class CorrectorTest(unittest.TestCase):

    def setUp(self):
        if BOTMCFFI:
            from BackOffTrigramModel import BackOffTrigramModelCFFI

            self.botm = BackOffTrigramModelCFFI.BackOffTMCFFI('code/correction/test/trigram_model_5K.arpa')
        else:
            raise "Whatever"

    def test_beam_search(self):

        tagged_sentence = [(u'This', 'DT'), (u'is', 'VBZ'), (u'a', 'DT'), (u'bad', 'JJ'), (u'sentence', 'NN'), (u'.', '.')]

        width = 5
        result = Corrector.beam_search(tagged_sentence, width, probability_of_error, path_probability_function, variation_generator)
        self.assertListEqual(result, [(u'This', 'DT'), (u'isa', 'VBZ'), (u'aa', 'DT'), (u'bad', 'JJ'), (u'sentence', 'NN')], result)

        width = 50
        result = Corrector.beam_search(tagged_sentence, width, probability_of_error, path_probability_function, variation_generator)
        self.assertListEqual(result, [(u'This', 'DT'), (u'isd', 'VBZ'), (u'aa', 'DT'), (u'bad', 'JJ'), (u'sentence', 'NN')], result)

        tagged_sentence = [(u'This', 'DT'), (u'is', 'VBZ'), (u'n\'t', 'RB'), (u'bad', 'JJ'), (u'...', ':')]
        result = Corrector.beam_search(tagged_sentence, width, probability_of_error, path_probability_function, variation_generator)
        self.assertListEqual(result, [(u'This', 'DT'), (u'isd', 'VBZ'), (u"n't", 'RB'), (u'bad', 'JJ'), (u'...', ':')], result)

    def test_ngram_path_probability(self):

        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)
        corrector = Corrector.Corrector(self.botm, 25, var_gen.generate_path_variations, -1.3)

        tokens = u'The I over'.split()
        tpp = corrector.ngram_path_probability(tokens)
        self.assertAlmostEqual(tpp, -4.185007, msg=tpp)

    def test_pos_ngram_path_probability(self):

        pos_ngram_server_obj = SRILMServerPipe.SRILMServerPipe('code/correction/test/pos_trigram_model_0K.arpa', '5') 
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)

        tagged_tokens = [(u'An', 'DT'), (u'elderly', 'JJ'), (u'person', 'NN')]

        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3, verbose=False, pos=1.0, pos_ngram_server_obj=pos_ngram_server_obj)
        ptpp = corrector.pos_ngram_path_probability(tagged_tokens)
        self.assertAlmostEqual(ptpp, -0.230294, msg=repr(ptpp))

        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3, verbose=False, pos=0.5, pos_ngram_server_obj=pos_ngram_server_obj)
        ptpp = corrector.pos_ngram_path_probability(tagged_tokens)
        self.assertAlmostEqual(ptpp, -0.7838715, msg=repr(ptpp))

    def test_closed_class_pos_ngram_path_probability(self):

        closed_class_pos_ngram_server_obj = SRILMServerPipe.SRILMServerPipe('code/correction/test/closed_class_order_5.arpa', '5')
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)

        tagged_tokens = [(u'An', 'DT'), (u'elderly', 'JJ'), (u'person', 'NN')]

        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3, verbose=False, closed_class=1.0, closed_class_pos_ngram_server_obj=closed_class_pos_ngram_server_obj, closed_class_tags=closed_class_tags, AUX=AUX)
        ptpp = corrector.closed_class_pos_ngram_path_probability(tagged_tokens)
        self.assertAlmostEqual(ptpp, -0.111492, msg=repr(ptpp))

        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3, verbose=False, closed_class=0.5, closed_class_pos_ngram_server_obj=closed_class_pos_ngram_server_obj, closed_class_tags=closed_class_tags, AUX=AUX)
        ptpp = corrector.closed_class_pos_ngram_path_probability(tagged_tokens)
        self.assertAlmostEqual(ptpp, -0.7244705, msg=repr(ptpp))

    def test_get_correction(self):
        '''
        This is a regression test and a test of pieces working
        together, not of the correctness of results.
        '''

        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)
        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3)

        tagged_sentence = [(u'I', 'PRP'), (u'agree', 'VBP'), (u'to', 'TO'), (u'a', 'DT'), (u'large', 'JJ'),(u'extent', 'NN'), (u'that', 'IN'), (u'current', 'JJ'), (u'policies', 'NNS'), (u'have', 'VBP'), (u'helped', 'VBN'), (u'to', 'TO'), (u'ease', 'VB'), (u'the', 'DT'), (u'aging', 'NN'), (u'process', 'NN'), (u'.', '.')]
        result = corrector.get_correction(tagged_sentence)
        self.assertListEqual(result, [(u'I', 'PRP'), (u'agree', 'VBP'), (u'to', 'TO'), (u'a', 'DT'), (u'large', 'JJ'), (u'extent', 'NN'), (u'that', 'IN'), (u'current', 'JJ'), (u'policies', 'NNS'), (u'have', 'VBP'), (u'helped', 'VBN'), (u'to', 'TO'), (u'ease', 'VB'), (u'the', 'DT'), (u'aging', 'NN'), (u'process', 'NN'), (u'.', '.')], result)

    def test_pos_correction(self):

        pos_ngram_server_obj = SRILMServerPipe.SRILMServerPipe('code/correction/test/pos_5-gram.arpa', '5')
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)
        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -2.3, verbose=False, pos=0.5, pos_ngram_server_obj=pos_ngram_server_obj)

        tagged_sentence = [(u'The', 'DT'), (u'goverment', 'NN'), (u'are', 'VBP'), (u'wrong', 'JJ'), (u'.', '.')]
        result = corrector.get_correction(tagged_sentence)
        self.assertListEqual(result, [(u'The', 'DT'), (u'goverment', 'NN'), (u'are', 'VBP'), (u'wrong', 'JJ'), (u'.', '.')], result)

        tagged_sentence = [(u'I', 'PRP'), (u'agree', 'VBP'), (u'to', 'TO'), (u'a', 'DT'), (u'large', 'JJ'), (u'extent', 'NN'), (u'that', 'IN'), (u'current', 'JJ'), (u'policies', 'NNS'), (u'have', 'VBP'), (u'helped', 'VBN'), (u'to', 'TO'), (u'ease', 'VB'), (u'the', 'DT'), (u'aging', 'NN'), (u'process', 'NN'), (u'.', '.')]
        result = corrector.get_correction(tagged_sentence)
        self.assertListEqual(result, [(u'I', 'PRP'), (u'agree', 'VBP'), (u'to', 'TO'), (u'a', 'DT'), (u'large', 'JJ'), (u'extent', 'NN'), (u'that', 'IN'), (u'current', 'JJ'), (u'policies', 'NNS'), (u'have', 'VBP'), (u'helped', 'VBN'), (u'to', 'TO'), (u'ease', 'VB'), (u'the', 'DT'), (u'aging', 'NN'), (u'process', 'NN'), (u'.', '.')], result)

    def test_closed_class_pos_correction(self):

        closed_class_pos_ngram_server_obj = SRILMServerPipe.SRILMServerPipe('code/correction/test/closed_class_order_5.arpa', '5')
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)
        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3, verbose=False, closed_class=0.5, closed_class_pos_ngram_server_obj=closed_class_pos_ngram_server_obj, closed_class_tags=closed_class_tags, AUX=AUX)

        tagged_sentence = [(u'The', 'DT'), (u'goverment', 'NN'), (u'are', 'VBP'), (u'wrong', 'JJ'), (u'.', '.')]
        result = corrector.get_correction(tagged_sentence)
        self.assertListEqual(result, [(u'The', 'DT'), (u'goverment', 'NN'), (u'are', 'VBP'), (u'wrong', 'JJ'), (u'.', '.')], result)



if __name__ == '__main__':
    unittest.main()
