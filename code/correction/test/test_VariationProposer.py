# L. Amber Wilcox-O'Hearn 2013
# test_VariationProposer.py

from code.correction import VariationProposer
from collections import defaultdict
from BackOffTrigramModel import BackOffTrigramModelPipe
import unittest

tag_dictionary = defaultdict(list)
tag_dictionary['DT'] = ["a", "the", "any", "another"]
tag_dictionary["IN"] = ["with", "from", "of"]
tag_dictionary["CC"] = ["and", "but", "or"]
tag_dictionary["VB"] = ["like", "love"]
tag_dictionary["VBD"] = ['loved']
tag_dictionary["VBG"] = ['loving']
tag_dictionary['TO'] = ['to']
tag_dictionary['MD'] = ['might', 'could']

insertables = ['of', 'from', 'could', 'a', 'the', 'are', 'engineering', 'waves', 'need']
deletables = ['with', 'a', 'the', 'water']

l_vars = ['laboured', 'labyrinths', 'laden', 'lamp', 'like', 'love', 'lover', 'loves', 'loving']

def vocab_with_prefix(prefix):
    if prefix == 'l':
        return l_vars
    if prefix == '':
        return ['am', 'are', 'bad', 'cue', 'did', 'is']
    return []

tmpipe_obj = BackOffTrigramModelPipe.BackOffTMPipe('BackOffTrigramModelPipe', 'code/correction/test/trigram_model_5K.arpa')

proposer = VariationProposer.VariationProposer(tag_dictionary, tmpipe_obj, insertables, deletables)

class VariationProposerTest(unittest.TestCase):

    def test_closed_class_alternatives(self):

        sentence = "We loved with a love that was more than love .".lower()
        tokens = sentence.split()
        tags = ['PRP', 'VBD', 'IN', 'DT', 'NN', 'WDT', 'VBD', 'JJR', 'IN', 'NN'][:len(sentence.split())]

        proposed = proposer.get_alternatives(tokens[0], tags[0])
        self.assertSetEqual(proposed, set([]), proposed)

        proposed = proposer.get_alternatives(tokens[1], tags[1])
        self.assertSetEqual(proposed, set([('love', 'VB')]), proposed)

        proposed = proposer.get_alternatives(tokens[2], tags[2])
        self.assertSetEqual(proposed, set([("from", 'IN'), ("of", 'IN'), ()]), proposed)

        proposed = proposer.get_alternatives(tokens[3], tags[3])
        self.assertSetEqual(proposed, set([("the", 'DT'), ("any", 'DT'), ("another", 'DT'), ()]), proposed)

    def test_levenshtein_distance(self):
        pass

    def test_generate_path_variations(self):
    #return ['PRP', 'VBD', 'IN', 'DT', 'NN', 'WDT', 'VBD', 'JJR', 'IN', 'NN'][:len(sentence.split())]

        tagged_sentence = [('We', 'PRP'), ('loved', 'VBD'), ('with', 'IN')]
        beginning = tagged_sentence[:-1]

        path_variations = proposer.generate_path_variations(tagged_sentence)
        self.assertEquals(len(path_variations), 21, str(path_variations) + ": " + str(len(path_variations)))
        self.assertIn(beginning, path_variations, path_variations)
        self.assertIn(beginning + [('a', 'DT'), ('from', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('a', 'DT'), ('of', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('the', 'DT'), ('from', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('the', 'DT'), ('of', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('of', 'IN'), ('from', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('of', 'IN'), ('of', 'IN')], path_variations, path_variations)

        self.assertIn(beginning + [('from', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('of', 'IN')], path_variations, path_variations)

        self.assertNotIn(beginning + [('another', 'DT'), ('from', 'IN')], path_variations, path_variations)
        self.assertNotIn(beginning + [('another', 'DT'), ('of', 'IN')], path_variations, path_variations)
        self.assertNotIn(beginning + [('with', 'IN')], path_variations, path_variations)

        tagged_sentence = [('We', 'PRP')]
        path_variations = proposer.generate_path_variations(tagged_sentence)
        self.assertIn([('Of', 'IN'), ('we', 'PRP')], path_variations, path_variations)

        tagged_sentence = [('Of', 'IN')]
        path_variations = proposer.generate_path_variations(tagged_sentence)
        self.assertIn([('Of', 'IN'), ('of', 'IN')], path_variations, path_variations)
        self.assertIn([('From', 'IN'), ('of', 'IN')], path_variations, path_variations)
        self.assertIn([('From', 'IN')], path_variations, path_variations)

if __name__ == '__main__':
    unittest.main()
