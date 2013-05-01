# L. Amber Wilcox-O'Hearn 2013
# test_VariationProposer.py

from code.correction import VariationProposer
from collections import defaultdict, Counter
from BackOffTrigramModel import BackOffTrigramModelPipe
import unittest

tag_dictionary = defaultdict(dict)
tag_dictionary['DT'] = {u"a": 22, u"the": 40, u"an": 30, u"this": 10, u"any": 2, u"another": 1}
tag_dictionary["IN"] = {u"with":40, u"from":40, u"of":40}
tag_dictionary["CC"] = {u"and":40, u"but":40, "or":40}
tag_dictionary["VB"] = {u"like":40, u"love":40, u'be':50, u'have':60}
tag_dictionary["VBD"] = {u'loved':40}
tag_dictionary["VBG"] = {u'loving':40}
tag_dictionary['TO'] = {u'to':40}
tag_dictionary['MD'] = {u'might':40, u'could':40}

l_vars = [u'laboured', u'labyrinths', u'laden', u'lamp', u'like', u'love', u'lover', u'loves', u'loving']

def vocab_with_prefix(prefix):
    if prefix == u'l':
        return l_vars
    if prefix == '':
        return [u'am', u'are', u'bad', u'cue', u'did', u'is']
    return []

tmpipe_obj = BackOffTrigramModelPipe.BackOffTMPipe('BackOffTrigramModelPipe', 'code/correction/test/trigram_model_5K.arpa')

proposer = VariationProposer.VariationProposer(tag_dictionary, tmpipe_obj)

class VariationProposerTest(unittest.TestCase):

    def test_dicts(self):

        self.assertDictEqual(proposer.closed_class_substitutables,
                             {'MD': [(u'could', 'MD'), (u'might', 'MD'), ()],
                              'DT': [(u'the', 'DT'), (u'an', 'DT'), (u'a', 'DT'), (u'this', 'DT'), (u'any', 'DT'), ()],
                              'AUX': [(u'be', 'VB'), (u'have', 'VB'), (u'to', 'TO'), ()],
                              'IN': [(u'with', 'IN'), (u'from', 'IN'), (u'of', 'IN'), (u'to', 'TO'), ()]},
                             proposer.closed_class_substitutables)

    def test_closed_class_alternatives(self):

        sentence = u"We loved with a love that was more than love .".lower()
        tokens = sentence.split()
        tags = ['PRP', 'VBD', 'IN', 'DT', 'NN', 'WDT', 'VBD', 'JJR', 'IN', 'NN'][:len(sentence.split())]

        proposed = proposer.get_alternatives(tokens[0], tags[0])
        self.assertSetEqual(set(proposed), set([]), proposed)

        proposed = proposer.get_alternatives(tokens[1], tags[1])
        self.assertSetEqual(set(proposed), set([(u'love', 'VB')]), proposed)

        proposed = proposer.get_alternatives(tokens[2], tags[2])
        self.assertSetEqual(set(proposed), set([(u"from", 'IN'), (u"of", 'IN'), (u'to', 'TO'), ()]), proposed)

        proposed = proposer.get_alternatives(tokens[3], tags[3])
        self.assertSetEqual(set(proposed), set([(u"the", 'DT'), (u"any", 'DT'), (u"this", 'DT'), (u"an", "DT"), ()]), proposed)

    def test_generate_path_variations(self):

        tagged_sentence = [(u'We', 'PRP'), (u'loved', 'VBD'), (u'with', 'IN')]
        beginning = tagged_sentence[:-1]
        err = -1.3

        path_variations, path_err = proposer.generate_path_variations(tagged_sentence, err)

        self.assertEquals(len(path_variations), 56, str(path_variations) + ": " + str(len(path_variations)))
        self.assertEquals(len(path_err), 56, str(path_variations) + ": " + str(len(path_err)))

        self.assertIn(beginning, path_variations, path_variations)
        index = path_variations.index(beginning)
        self.assertAlmostEqual(path_err[index], -1.9020599913279623, 5, msg=path_err[index])

        self.assertIn(beginning + [(u'a', 'DT'), (u'from', 'IN')], path_variations, path_variations)
        index = path_variations.index(beginning + [(u'a', 'DT'), (u'from', 'IN')])
        self.assertAlmostEqual(path_err[index], -3.9010299956639813, 5, msg=path_err[index])

        self.assertIn(beginning + [(u'a', 'DT'), (u'with', 'IN')], path_variations, path_variations)
        index = path_variations.index(beginning + [(u'a', 'DT'), (u'with', 'IN')])
        self.assertAlmostEqual(path_err[index], -2.0213006770718103, 5, msg=path_err[index])

        self.assertIn(beginning + [(u'a', 'DT'), (u'of', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [(u'the', 'DT'), (u'from', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [(u'the', 'DT'), (u'of', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [(u'of', 'IN'), (u'from', 'IN')], path_variations, path_variations)
        self.assertIn(beginning + [(u'of', 'IN'), (u'of', 'IN')], path_variations, path_variations)

        self.assertIn(beginning + [(u'from', 'IN')], path_variations, path_variations)
        index = path_variations.index(beginning + [(u'from', 'IN')])
        self.assertAlmostEqual(path_err[index], -1.9020599913279623, 5, msg=path_err[index])

        self.assertIn(beginning + [(u'of', 'IN')], path_variations, path_variations)

        self.assertNotIn(beginning + [(u'another', 'DT'), (u'from', 'IN')], path_variations, path_variations)
        self.assertNotIn(beginning + [(u'another', 'DT'), (u'of', 'IN')], path_variations, path_variations)
        self.assertNotIn(beginning + [(u'with', 'IN')], path_variations, path_variations)

        tagged_sentence = [(u'We', 'PRP')]
        path_variations, path_err = proposer.generate_path_variations(tagged_sentence, err)
        self.assertIn([(u'Of', 'IN'), (u'we', 'PRP')], path_variations, path_variations)

        tagged_sentence = [(u'Of', 'IN')]
        path_variations, path_err = proposer.generate_path_variations(tagged_sentence, err)
        self.assertIn([(u'Of', 'IN'), (u'of', 'IN')], path_variations, path_variations)
        self.assertIn([(u'From', 'IN'), (u'of', 'IN')], path_variations, path_variations)
        self.assertIn([(u'From', 'IN')], path_variations, path_variations)

if __name__ == '__main__':
    unittest.main()
