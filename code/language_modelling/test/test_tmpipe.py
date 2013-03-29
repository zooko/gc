#!/usr/bin/env python

from code.language_modelling import tmpipe
import unittest, sys

unkless_tmpipe_obj = tmpipe.TMPipe("code/language_modelling/tmPipe", "code/language_modelling/test/pos_trigram_model_0.05K.arpa")
unkful_tmpipe_obj = tmpipe.TMPipe("code/language_modelling/tmPipe", "code/language_modelling/test/trigram_model_0.1K.arpa")

DECIMAL_PLACES = 5

class TmpipeUnklessTest(unittest.TestCase):

    def test_in_vocabulary(self):
        assert unkless_tmpipe_obj.in_vocabulary('"')
        assert unkless_tmpipe_obj.in_vocabulary("'s")
        assert unkless_tmpipe_obj.in_vocabulary('with')
        assert not unkless_tmpipe_obj.in_vocabulary('wax')

    def test_unigram_probability(self):
        probability = unkless_tmpipe_obj.unigram_probability('"')
        self.assertAlmostEqual(probability, -2.589533, DECIMAL_PLACES, msg=probability)

        probability = unkless_tmpipe_obj.unigram_probability("'s")
        self.assertAlmostEqual(probability, -2.52453, DECIMAL_PLACES, msg=probability)

        probability = unkless_tmpipe_obj.unigram_probability('with')
        self.assertAlmostEqual(probability, -2.395761, DECIMAL_PLACES, msg=probability)

        probability = unkless_tmpipe_obj.unigram_probability('wax')
        self.assertIs(probability, None, msg=probability)

class TmpipeUnkfulTest(unittest.TestCase):

    def test_unigram_probability(self):
        probability = unkful_tmpipe_obj.unigram_probability('"')
        self.assertAlmostEqual(probability, -2.589533, DECIMAL_PLACES, msg=probability)

        probability = unkful_tmpipe_obj.unigram_probability("'s")
        self.assertAlmostEqual(probability, -2.52453, DECIMAL_PLACES, msg=probability)

        probability = unkful_tmpipe_obj.unigram_probability('with')
        self.assertAlmostEqual(probability, -2.325526, DECIMAL_PLACES, msg=probability)

        probability = unkful_tmpipe_obj.unigram_probability('wax')
        self.assertAlmostEqual(probability, -0.3612903, DECIMAL_PLACES, msg=probability)

    def test_trigram_probability(self):
        self.skipTest("")

if __name__ == '__main__':
    unittest.main()
