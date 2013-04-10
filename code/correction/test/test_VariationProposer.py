# L. Amber Wilcox-O'Hearn 2013
# test_VariationProposer.py

from code.correction import VariationProposer
import unittest

tag_dictionary = {"DT": ["a", "the", "any", "another", ""], "IN": ["with", "from", "of", ""], "CC": ["and", "but", "or"], "VB": ["like", "love"], "VBD": ['loved'], "VBG": ['loving']}

def pos_tagger(tokens):
    return ['PRP', 'VBD', 'IN', 'DT', 'NN', 'WDT', 'VBD', 'JJR', 'IN', 'NN'][:len(tokens)]

l_vars = ['laboured', 'labyrinths', 'laden', 'lamp', 'like', 'love', 'lover', 'loves', 'loving']

def vocab_with_prefix(prefix):
    if prefix == 'l':
        return l_vars
    if prefix == '':
        return ['am', 'are', 'bad', 'cue', 'did', 'is']
    return []

proposer = VariationProposer.VariationProposer(pos_tagger, tag_dictionary, vocab_with_prefix)

class VariationProposerTest(unittest.TestCase):

    def test_closed_class_alternatives(self):

        tokens = "We loved with a love that was more than love .".lower().split()
        tags = pos_tagger(tokens)

        proposed = proposer.get_alternatives(tokens[0], tags[0])
        self.assertListEqual(proposed, [])

        proposed = proposer.get_alternatives(tokens[1], tags[1])
        self.assertListEqual(proposed, ['like', 'love', 'loving'])

        proposed = proposer.get_alternatives(tokens[2], tags[2])
        self.assertListEqual(proposed, ["from", "of", ""], proposed)

        proposed = proposer.get_alternatives(tokens[3], tags[3])
        self.assertListEqual(proposed, ["the", "any", "another", ""], proposed)






if __name__ == '__main__':
    unittest.main()
