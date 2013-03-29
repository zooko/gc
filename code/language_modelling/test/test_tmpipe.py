#!/usr/bin/env python

import tmpipe, unittest
import sys

EPSILON = .0000001

tmpipeobj = tmpipe.TMPipe("../src/c/tmPipe", "data/mini.arpa")

class TmpipeTest(unittest.TestCase):
    def test_trigram_probability(self):
        tmpipeobj.stdin.write('t , " says\n')
        l = tmpipeobj.stdout.readline()
        assert abs(-0.659269 - float(l)) < EPSILON, l
        tmpipeobj.stdin.write("t it will be\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-1.009832 - float(l)) < EPSILON, l
        tmpipeobj.stdin.write("t it will not\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-2.440987 - float(l)) < EPSILON, l

    def test_unigram_probability(self):
        tmpipeobj.stdin.write('u "\n')
        l = tmpipeobj.stdout.readline()
        assert abs(-2.187073 - float(l)) < EPSILON, l
        tmpipeobj.stdin.write('u &\n')
        l = tmpipeobj.stdout.readline()
        assert abs(-2.799857 - float(l)) < EPSILON, l
        tmpipeobj.stdin.write("u it\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-2.1371 - float(l)) < EPSILON, l
        tmpipeobj.stdin.write("u zero\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-3.799857 - float(l)) < EPSILON, l
        
    def test_unigram_backoff(self):
        tmpipeobj.stdin.write("o it\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-0.260354 - float(l)) < EPSILON, l
        tmpipeobj.stdin.write("o zero\n")
        l = tmpipeobj.stdout.readline()
        assert abs(-0.2765851 - float(l)) < EPSILON, l
        

if __name__ == '__main__':
    unittest.main()
