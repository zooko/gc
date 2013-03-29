#!/usr/bin/env python

from code.language_modelling import tmpipe
import unittest, sys

tmpipe_obj = tmpipe.TMPipe("code/language_modelling/tmPipe", "code/language_modelling/test/pos_trigram_model_0.05K.arpa")

class TmpipeUnklessTest(unittest.TestCase):

    def test_in_vocabulary(self):
        assert tmpipe_obj.in_vocabulary('"')
        assert tmpipe_obj.in_vocabulary("'s")
        assert tmpipe_obj.in_vocabulary('with')
        assert not tmpipe_obj.in_vocabulary('wax')

    def test_unigram_probability(self):
        probability = tmpipe_obj.unigram_probability('"')
        self.assertAlmostEqual(probability, -2.589533, probability)

        probability = tmpipe_obj.unigram_probability("'s")
        self.assertAlmostEqual(probability, -2.52453, probability)

        probability = tmpipe_obj.unigram_probability('with')
        self.assertAlmostEqual(probability, -2.395761, probability)

        probability = tmpipe_obj.unigram_probability('wax')
        self.assertIs(probability, None, probability)


    def test_trigram_probability(self):
        self.skipTest("")
        tmpipeobj.stdin.write('t , " says\n')
        l = tmpipeobj.stdout.readline()
        assert abs(-0.659269 - float(l)) < EPSILON, l
        tmpipeobj.stdin.write("t it will be\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-1.009832 - float(l)) < EPSILON, l
        tmpipeobj.stdin.write("t it will not\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-2.440987 - float(l)) < EPSILON, l

    def test_unigram_backoff(self):
        self.skipTest("")
        tmpipeobj.stdin.write("o it\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-0.260354 - float(l)) < EPSILON, l
        tmpipeobj.stdin.write("o zero\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-0.2765851 - float(l)) < EPSILON, l
        

if __name__ == '__main__':
    unittest.main()
