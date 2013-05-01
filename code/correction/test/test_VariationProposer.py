# L. Amber Wilcox-O'Hearn 2013
# test_VariationProposer.py

from code.correction import VariationProposer
from collections import defaultdict, Counter
from BackOffTrigramModel import BackOffTrigramModelPipe
import unittest

tag_dictionary = defaultdict(dict)
tag_dictionary['DT'] = {"a": 22, "the": 40, "an": 30, "this": 10, "any": 2, "another": 1}
tag_dictionary["IN"] = {"with":40, "from":40, "of":40}
tag_dictionary["CC"] = {"and":40, "but":40, "or":40}
tag_dictionary["VB"] = {"like":40, "love":40, 'be':50, 'have':60}
tag_dictionary["VBD"] = {'loved':40}
tag_dictionary["VBG"] = {'loving':40}
tag_dictionary['TO'] = {'to':40}
tag_dictionary['MD'] = {'might':40, 'could':40}

l_vars = ['laboured', 'labyrinths', 'laden', 'lamp', 'like', 'love', 'lover', 'loves', 'loving']

def vocab_with_prefix(prefix):
    if prefix == 'l':
        return l_vars
    if prefix == '':
        return ['am', 'are', 'bad', 'cue', 'did', 'is']
    return []

tmpipe_obj = BackOffTrigramModelPipe.BackOffTMPipe('BackOffTrigramModelPipe', 'code/correction/test/trigram_model_5K.arpa')

proposer = VariationProposer.VariationProposer(tag_dictionary, tmpipe_obj)

class VariationProposerTest(unittest.TestCase):

    def test_dicts(self):

        self.assertDictEqual(proposer.closed_class_substitutables,
                             {'MD': [('could', 'MD'), ('might', 'MD'), ()],
                              'DT': [('the', 'DT'), ('an', 'DT'), ('a', 'DT'), ('this', 'DT'), ('any', 'DT'), ()],
                              'AUX': [('be', 'VB'), ('have', 'VB'), ('to', 'TO'), ()],
                              'IN': [('with', 'IN'), ('from', 'IN'), ('of', 'IN'), ('to', 'TO'), ()]},
                             proposer.closed_class_substitutables)

    def test_closed_class_alternatives(self):

        sentence = "We loved with a love that was more than love .".lower()
        tokens = sentence.split()
        tags = ['PRP', 'VBD', 'IN', 'DT', 'NN', 'WDT', 'VBD', 'JJR', 'IN', 'NN'][:len(sentence.split())]

        proposed = proposer.get_alternatives(tokens[0], tags[0])
        self.assertSetEqual(set(proposed), set([]), proposed)

        proposed = proposer.get_alternatives(tokens[1], tags[1])
        self.assertSetEqual(set(proposed), set([('love', 'VB')]), proposed)

        proposed = proposer.get_alternatives(tokens[2], tags[2])
        self.assertSetEqual(set(proposed), set([("from", 'IN'), ("of", 'IN'), ('to', 'TO'), ()]), proposed)

        proposed = proposer.get_alternatives(tokens[3], tags[3])
        self.assertSetEqual(set(proposed), set([("the", 'DT'), ("any", 'DT'), ("this", 'DT'), ("an", "DT"), ()]), proposed)

    def test_generate_path_variations(self):

        tagged_sentence = [('We', 'PRP'), ('loved', 'VBD'), ('with', 'IN')]
        beginning = tagged_sentence[:-1]
        err = -1.3

        path_variations, path_err = proposer.generate_path_variations(tagged_sentence, err)

        self.assertEquals(len(path_variations), 56, str(path_variations) + ": " + str(len(path_variations)))
        self.assertEquals(len(path_err), 56, str(path_variations) + ": " + str(len(path_err)))

        self.assertIn(beginning, path_variations, path_variations)
        index = path_variations.index(beginning)
        self.assertAlmostEqual(path_err[index], -1.9020599913279623, 5, msg=path_err[index])

        self.assertIn(beginning + [('a', 'DT'), ('from', 'IN')], path_variations, path_variations)
        index = path_variations.index(beginning + [('a', 'DT'), ('from', 'IN')])
        self.assertAlmostEqual(path_err[index], -3.9010299956639813, 5, msg=path_err[index])

        self.assertIn(beginning + [('a', 'DT'), ('with', 'IN')], path_variations, path_variations)
        index = path_variations.index(beginning + [('a', 'DT'), ('with', 'IN')])
        self.assertAlmostEqual(path_err[index], -2.0213006770718103, 5, msg=path_err[index])

        self.assertIn(beginning + [('a', 'DT'), ('of', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('the', 'DT'), ('from', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('the', 'DT'), ('of', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('of', 'IN'), ('from', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [('of', 'IN'), ('of', 'IN')], path_variations, path_variations)

        self.assertIn(beginning + [('from', 'IN')], path_variations, path_variations)
        index = path_variations.index(beginning + [('from', 'IN')])
        self.assertAlmostEqual(path_err[index], -1.9020599913279623, 5, msg=path_err[index])

        self.assertIn(beginning + [('of', 'IN')], path_variations, path_variations)

        self.assertNotIn(beginning + [('another', 'DT'), ('from', 'IN')], path_variations, path_variations)
        self.assertNotIn(beginning + [('another', 'DT'), ('of', 'IN')], path_variations, path_variations)
        self.assertNotIn(beginning + [('with', 'IN')], path_variations, path_variations)

        tagged_sentence = [('We', 'PRP')]
        path_variations, path_err = proposer.generate_path_variations(tagged_sentence, err)
        self.assertIn([('Of', 'IN'), ('we', 'PRP')], path_variations, path_variations)

        tagged_sentence = [('Of', 'IN')]
        path_variations, path_err = proposer.generate_path_variations(tagged_sentence, err)
        self.assertIn([('Of', 'IN'), ('of', 'IN')], path_variations, path_variations)
        self.assertIn([('From', 'IN'), ('of', 'IN')], path_variations, path_variations)
        self.assertIn([('From', 'IN')], path_variations, path_variations)

if __name__ == '__main__':
    unittest.main()
