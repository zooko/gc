# L. Amber Wilcox-O'Hearn 2013
# test_POSFiller.py

from code.preprocessing import POSFiller
import unittest

class POSFillerTest(unittest.TestCase):

    def test_pos_fill_sentence(self):

        def in_vocabulary_0(token):
            return token != "will"

        def in_vocabulary_1(token):
            return token != "will" and token != "caused"

        def pos_tagger(sentence):
            psos = []
            for i in range(len(sentence)):
                if i % 2 == 0:
                    psos.append("NN")
                else:
                    psos.append("VBN")
            return psos
                
                          
        sentence = " ".join(["This", "will", "caused", "problems", "."])
        filled = POSFiller.fill_sentence([in_vocabulary_0, in_vocabulary_1], pos_tagger, sentence)
        self.assertListEqual(filled, [["This", "VBN", "caused", "problems", "."], ["This", "VBN", "NN", "problems", "."]], filled)
        
        

if __name__ == '__main__':
    unittest.main()
