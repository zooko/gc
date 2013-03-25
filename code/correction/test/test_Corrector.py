# L. Amber Wilcox-O'Hearn 2013
# test_Corrector.py

from code.correction import Corrector
import unittest 

class SentencePathTest(unittest.TestCase):

    def test_sentence_path(self):
        path = Corrector.SentencePath('This', -.7, None)
        new_path = Corrector.SentencePath('is', -.8, path)
        newer_path = Corrector.SentencePath('fun', -1.1, new_path)

        self.assertEqual(repr(path), "<SentencePath [('This', -0.7)]>", path)
        self.assertEqual(repr(new_path), "<SentencePath [('This', -0.7), ('is', -0.8)]>", new_path)
        self.assertEqual(repr(newer_path), "<SentencePath [('This', -0.7), ('is', -0.8), ('fun', -1.1)]>", newer_path)
        self.assertListEqual(path.tokens(), ['This'], path.tokens())
        self.assertListEqual(new_path.tokens(), ['This', 'is'], new_path.tokens())
        self.assertListEqual(newer_path.tokens(), ['This', 'is', 'fun'], newer_path.tokens())
        a_list = [new_path, newer_path, path]
        a_list.sort()
        self.assertListEqual(a_list, [newer_path, new_path, path], a_list)
        
class BeamTest(unittest.TestCase):

    def test_beam(self):
        self.skipTest("")
        

if __name__ == '__main__':
    unittest.main()
