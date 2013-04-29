# L. Amber Wilcox-O'Hearn 2013
# test_Corrector.py

from code.language_modelling import SRILMServerPipe
from code.correction import Corrector, VariationProposer
import unittest, json

def probability_of_error_function():
    return 0.01
def variation_generator(tagged_sentence):
    tokens = [t[0] for t in tagged_sentence]
    tags = [t[1] for t in tagged_sentence]
    token = tokens[-1]
    if len(token) > 2:
        return [ ]
    else:
        if token == '.':
            return [ tagged_sentence[:-1] + [(var, tags[-1])] for var in  [token + x for x in 'abcde'] ] + [ tagged_sentence[:-1] ]
        else:
            return [ tagged_sentence[:-1] + [(var, tags[-1])] for var in  [token + x for x in 'abcde'] ]
def path_probability_function(tagged_tokens):
    tokens = [t[0] for t in tagged_tokens]
    num_a_s = tokens[-1].count('a')
    if len(tokens) > 3 and tokens[1] == 'isd':
        return 1 + .9 ** (len(tokens[-1]) - num_a_s) * .999999 ** num_a_s - len(tokens)
    return .9 ** (len(tokens[-1]) - num_a_s) * .999999 ** num_a_s - len(tokens)

stanford_tagger_path = 'stanford-tagger/stanford-postagger.jar:'
module_path = 'edu.stanford.nlp.tagger.maxent.MaxentTagger'
model_path = 'stanford-tagger/english-left3words-distsim.tagger'
closed_class_tags = ['IN', 'DT', 'TO', 'MD']
AUX = ['be', 'is', 'are', 'were', 'was', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'get', 'got', 'getting']

BOTMCFFI=True

class CorrectorTest(unittest.TestCase):

    def setUp(self):
        if BOTMCFFI:
            from BackOffTrigramModel import BackOffTrigramModelCFFI

            self.botm = BackOffTrigramModelCFFI.BackOffTMCFFI('code/correction/test/trigram_model_5K.arpa')
        else:
            raise "Whatever"

    def test_beam_search(self):

        tagged_sentence = [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('bad', 'JJ'), ('sentence', 'NN'), ('.', '.')]

        width = 5
        result = Corrector.beam_search(tagged_sentence, width, probability_of_error_function, path_probability_function, variation_generator)
        self.assertListEqual(result, [('This', 'DT'), ('isa', 'VBZ'), ('aa', 'DT'), ('bad', 'JJ'), ('sentence', 'NN')], result)

        width = 50
        result = Corrector.beam_search(tagged_sentence, width, probability_of_error_function, path_probability_function, variation_generator)
        self.assertListEqual(result, [('This', 'DT'), ('isd', 'VBZ'), ('aa', 'DT'), ('bad', 'JJ'), ('sentence', 'NN')], result)

        tagged_sentence = [('This', 'DT'), ('is', 'VBZ'), ('n\'t', 'RB'), ('bad', 'JJ'), ('...', ':')]
        result = Corrector.beam_search(tagged_sentence, width, probability_of_error_function, path_probability_function, variation_generator)
        self.assertListEqual(result, [('This', 'DT'), ('isd', 'VBZ'), ("n't", 'RB'), ('bad', 'JJ'), ('...', ':')], result)

    def test_ngram_path_probability(self):

        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)
        corrector = Corrector.Corrector(self.botm, 25, var_gen.generate_path_variations, -1.3)

        tokens = u'The I over'.split()
        tpp = corrector.ngram_path_probability(tokens)
        self.assertAlmostEqual(tpp, -4.185007, msg=tpp)

    def test_pos_ngram_path_probability(self):

        pos_ngram_server_obj = SRILMServerPipe.SRILMServerPipe('7878', 'code/correction/test/pos_trigram_model_0K.arpa', '5')
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)

        tagged_tokens = [(u'An', u'DT'), (u'elderly', u'JJ'), (u'person', u'NN')]

        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3, verbose=False, pos=1.0, pos_ngram_server_obj=pos_ngram_server_obj)
        ptpp = corrector.pos_ngram_path_probability(tagged_tokens)
        self.assertAlmostEqual(ptpp, -0.230294, msg=repr(ptpp))

        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3, verbose=False, pos=0.5, pos_ngram_server_obj=pos_ngram_server_obj)
        ptpp = corrector.pos_ngram_path_probability(tagged_tokens)
        self.assertAlmostEqual(ptpp, -0.7838715, msg=repr(ptpp))

    def test_closed_class_pos_ngram_path_probability(self):

        closed_class_pos_ngram_server_obj = SRILMServerPipe.SRILMServerPipe('1234', 'code/correction/test/closed_class_order_5.arpa', '5')
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)

        tagged_tokens = [(u'An', u'DT'), (u'elderly', u'JJ'), (u'person', u'NN')]

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

        tagged_sentence = [('I', 'PRP'), ('agree', 'VBP'), ('to', 'TO'), ('a', 'DT'), ('large', 'JJ'),('extent', 'NN'), ('that', 'IN'), ('current', 'JJ'), ('policies', 'NNS'), ('have', 'VBP'), ('helped', 'VBN'), ('to', 'TO'), ('ease', 'VB'), ('the', 'DT'), ('aging', 'NN'), ('process', 'NN'), ('.', '.')]
        result = corrector.get_correction(tagged_sentence)
        self.assertListEqual(result, [('I', 'PRP'), ('agree', 'VBP'), ('to', 'TO'), ('a', 'DT'), ('large', 'JJ'), ('extent', 'NN'), ('that', 'IN'), ('current', 'JJ'), ('policies', 'NNS'), ('have', 'VBP'), ('helped', 'VBN'), ('to', 'TO'), ('ease', 'VB'), ('the', 'DT'), ('aging', 'NN'), ('process', 'NN'), ('.', '.')], result)

    def test_pos_correction(self):

        pos_ngram_server_obj = SRILMServerPipe.SRILMServerPipe('8488', 'code/correction/test/pos_5-gram.arpa', '5')
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)
        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3, verbose=False, pos=0.5, pos_ngram_server_obj=pos_ngram_server_obj)

        tagged_sentence = [('The', 'DT'), ('goverment', 'NN'), ('are', 'VBP'), ('wrong', 'JJ'), ('.', '.')]
        result = corrector.get_correction(tagged_sentence)
        self.assertListEqual(result, [('The', 'DT'), ('goverment', 'NN'), ('is', 'VBZ'), ('wrong', 'JJ'), ('.', '.')], result)

        tagged_sentence = [('I', 'PRP'), ('agree', 'VBP'), ('to', 'TO'), ('a', 'DT'), ('large', 'JJ'), ('extent', 'NN'), ('that', 'IN'), ('current', 'JJ'), ('policies', 'NNS'), ('have', 'VBP'), ('helped', 'VBN'), ('to', 'TO'), ('ease', 'VB'), ('the', 'DT'), ('aging', 'NN'), ('process', 'NN'), ('.', '.')]
        result = corrector.get_correction(tagged_sentence)
        self.assertListEqual(result, [('I', 'PRP'), ('agree', 'VBP'), ('to', 'TO'), ('a', 'DT'), ('large', 'JJ'), ('extent', 'NN'), ('that', 'IN'), ('current', 'JJ'), ('policies', 'NNS'), ('have', 'VBP'), ('helped', 'VBN'), ('to', 'TO'), ('ease', 'VB'), ('the', 'DT'), ('aging', 'NN'), ('process', 'NN'), ('.', '.')], result)

    def test_closed_class_pos_correction(self):

        closed_class_pos_ngram_server_obj = SRILMServerPipe.SRILMServerPipe('5888', 'code/correction/test/closed_class_order_5.arpa', '5')
        pos_dictionary = json.load(open('code/correction/test/pos_dictionary', 'r'))
        var_gen = VariationProposer.VariationProposer(pos_dictionary, self.botm)
        corrector = Corrector.Corrector(self.botm, 5, var_gen.generate_path_variations, -1.3, verbose=False, closed_class=0.5, closed_class_pos_ngram_server_obj=closed_class_pos_ngram_server_obj, closed_class_tags=closed_class_tags, AUX=AUX)

        tagged_sentence = [('The', 'DT'), ('goverment', 'NN'), ('are', 'VBP'), ('wrong', 'JJ'), ('.', '.')]
        result = corrector.get_correction(tagged_sentence)
        self.assertListEqual(result, [('The', 'DT'), ('goverment', 'NN'), ('is', 'VBZ'), ('wrong', 'JJ'), ('.', '.')], result)



if __name__ == '__main__':
    unittest.main()
