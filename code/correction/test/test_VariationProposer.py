# L. Amber Wilcox-O'Hearn 2013
# test_VariationProposer.py

from code.correction import VariationProposer
from collections import defaultdict
import unittest

tag_dictionary = defaultdict(list)
tag_dictionary['DT'] = ["a", "the", "any", "another"]
tag_dictionary["IN"] = ["with", "from", "of", '']
tag_dictionary["CC"] = ["and", "but", "or"]
tag_dictionary["VB"] = ["like", "love"]
tag_dictionary["VBD"] = ['loved']
tag_dictionary["VBG"] = ['loving']
tag_dictionary['TO'] = ['to']
tag_dictionary['MD'] = ['might', 'could']

insertables = ['of', 'from', 'could', 'a', 'the', 'are', 'engineering', 'waves', 'need']

def pos_tagger(sentence):
    return ['PRP', 'VBD', 'IN', 'DT', 'NN', 'WDT', 'VBD', 'JJR', 'IN', 'NN'][:len(sentence.split())]

l_vars = ['laboured', 'labyrinths', 'laden', 'lamp', 'like', 'love', 'lover', 'loves', 'loving']

def vocab_with_prefix(prefix):
    if prefix == 'l':
        return l_vars
    if prefix == '':
        return ['am', 'are', 'bad', 'cue', 'did', 'is']
    return []

proposer = VariationProposer.VariationProposer(pos_tagger, tag_dictionary, vocab_with_prefix, insertables)

class VariationProposerTest(unittest.TestCase):

    def test_closed_class_alternatives(self):

        sentence = "We loved with a love that was more than love .".lower()
        tokens = sentence.split()
        tags = pos_tagger(sentence)

        proposed = proposer.get_alternatives(tokens[0], tags[0])
        self.assertListEqual(proposed, [])

        proposed = proposer.get_alternatives(tokens[1], tags[1])
        self.assertListEqual(proposed, ['like', 'love', 'loving'])

        proposed = proposer.get_alternatives(tokens[2], tags[2])
        self.assertListEqual(proposed, ["from", "of", ""], proposed)

        proposed = proposer.get_alternatives(tokens[3], tags[3])
        self.assertListEqual(proposed, ["the", "any", "another"], proposed)

    def test_generate_path_variations(self):

        sentence = "We loved with".lower()
        tokens = sentence.split()
        beginning = tokens[:-1]

        path_variations = proposer.generate_path_variations(sentence)
        self.assertEquals(len(path_variations), 21, str(path_variations) + ": " + str(len(path_variations)))
        self.assertIn(beginning, path_variations, path_variations)
        self.assertIn(beginning + ['a', 'from'], path_variations, path_variations)
        self.assertIn(beginning + ['a', 'of'], path_variations, path_variations)
        self.assertIn(beginning + ['the', 'from'], path_variations, path_variations)
        self.assertIn(beginning + ['the', 'of'], path_variations, path_variations)
        self.assertIn(beginning + ['of', 'from'], path_variations, path_variations)
        self.assertIn(beginning + ['of', 'of'], path_variations, path_variations)

        self.assertIn(beginning + ['from'], path_variations, path_variations)
        self.assertIn(beginning + ['of'], path_variations, path_variations)

        self.assertNotIn(beginning + ['another', 'from'], path_variations, path_variations)
        self.assertNotIn(beginning + ['another', 'of'], path_variations, path_variations)
        self.assertNotIn(beginning + ['with'], path_variations, path_variations)

if __name__ == '__main__':
    unittest.main()
