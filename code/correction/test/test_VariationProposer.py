# L. Amber Wilcox-O'Hearn 2013
# test_VariationProposer.py

from code.correction import VariationProposer
import unittest

tags = ["CC", "DT ", "IN ", "JJ ", "MD ", "NN ", "NNS", "VB ", "."]
tag_dictionary = {"DT": ["a", "the", "any", "another", ""], "IN": ["with", "from", "of", ""], "CC": ["and", "but", "or"]}

def pos_tagger(tokens):
    return ['PRP', 'VBD', 'IN', 'DT', 'NN', 'WDT', 'VBD', 'JJR', 'IN', 'NN'][:len(tokens)]
    

proposer = VariationProposer.VariationProposer(pos_tagger, tag_dictionary)

class VariationProposerTest(unittest.TestCase):

    def test_closed_class_alternatives(self):
        
        tokens = "We loved with a love that was more than love .".lower().split()

        proposed = proposer.closed_class_alternatives(tokens[:1])
        self.assertListEqual(proposed, [])

        proposed = proposer.closed_class_alternatives(tokens[:2])
        self.assertListEqual(proposed, [])

        proposed = proposer.closed_class_alternatives(tokens[:3])
        self.assertListEqual(proposed, ["from", "of", ""], proposed)

        proposed = proposer.closed_class_alternatives(tokens[:4])
        self.assertListEqual(proposed, ["the", "any", "another", ""], proposed)
    
        




if __name__ == '__main__':
    unittest.main()
