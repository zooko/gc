# L. Amber Wilcox-O'Hearn 2013
# test_StanfordTaggerPipe.py

from code.preprocessing import NLTKTagger
import unittest

class StanfordTaggerPipeTest(unittest.TestCase):

    def setUp(self):

        self.s0 = u"Hello , World .\n"
        self.s1 = u"Hello again , World .\n"
        self.s2 = u"- { http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php } [ HYPERLINK : http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php ]\n"
        self.s3 = u"Hence the RTI system is very inexpensively and can be commonly used ( Retinal Technologies , Inc. Launches Company and Revolutionizes Biometrics With Patented Retinal Scanning Technology , 2001 ) ."
        self.tagger = NLTKTagger.NLTKTagger()

    def test_words_and_tags_list(self):

        words_and_tags_list = self.tagger.words_and_tags_list(self.s0)
        self.assertEqual(words_and_tags_list, [(u'Hello', 'UH'), (u',', ','), (u'World', 'NNP'), (u'.', '.')], words_and_tags_list)
        words_and_tags_list = self.tagger.words_and_tags_list(self.s1)
        self.assertEqual(words_and_tags_list, \
          [('Hello', 'UH'), ('again', 'RB'), (',', ','), ('World', 'NNP'), ('.', '.')],  \
             words_and_tags_list)
        words_and_tags_list = self.tagger.words_and_tags_list(self.s2)
        self.assertListEqual(words_and_tags_list, \
             [('-', ':'), ('-LRB-', '-LRB-'), ('http', 'JJ'), (':', ':'), ('//uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php', 'NN'), ('-RRB-', '-RRB-'), ('-LRB-', '-LRB-'), ('HYPERLINK', 'NN'), (':', ':'), ('http', 'NN'), (':', ':'), ('//uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php', 'NN'), ('-RRB-', '-RRB-')], \
             words_and_tags_list)

    def test_multi_sentence_line(self):
        multi_sentence = u'I am .  More than one .\n'
        words_and_tags_list = self.tagger.words_and_tags_list(multi_sentence)
        self.assertListEqual(words_and_tags_list, [(u'I', 'PRP'), (u'am', 'VBP'), (u'.', '.'), (u'More', 'JJR'), (u'than', 'IN'), (u'one', 'CD'), (u'.', '.')], words_and_tags_list)
        for i in words_and_tags_list:
            self.assertIsInstance(i[0], unicode, i)
            self.assertIsInstance(i[1], unicode, i)

    def test_unicode(self):
        unicode_sentence = '496e204275726d6573652063756973696e65202c2061207377656574206a656c6c79206b6e6f776e2061732022206b7961756b206b7961772022202820e2808b20e180b120e1808020e180bb20e180ac20e1808020e180ba20e2808b20e180b120e1808020e180bc20e180ac205b207420ca8320616f20ca94207420ca83206175205d2029206973206d6164652066726f6d2061676172202e0a'.decode('hex').decode('utf-8')
        words_and_tags_list = self.tagger.words_and_tags_list(unicode_sentence)
        self.assertListEqual(words_and_tags_list, [(u'In', 'IN'), (u'Burmese', 'NNP'), (u'cuisine', 'NN'), (u',', ','), (u'a', 'DT'), (u'sweet', 'JJ'), (u'jelly', 'RB'), (u'known', 'VBN'), (u'as', 'IN'), (u'"', 'NNP'), (u'kyauk', 'NN'), (u'kyaw', 'NN'), (u'"', ':'), (u'(', ':'), (u'\u200b', ':'), (u'\u1031', ':'), (u'\u1000', ':'), (u'\u103b', ':'), (u'\u102c', ':'), (u'\u1000', ':'), (u'\u103a', ':'), (u'\u200b', ':'), (u'\u1031', ':'), (u'\u1000', ':'), (u'\u103c', ':'), (u'\u102c', ':'), (u'[', ':'), (u't', 'NN'), (u'\u0283', ':'), (u'ao', 'NN'), (u'\u0294', ':'), (u't', 'NN'), (u'\u0283', ':'), (u'au', 'NN'), (u']', ':'), (u')', ':'), (u'is', 'VBZ'), (u'made', 'VBN'), (u'from', 'IN'), (u'agar', 'NN'), (u'.', '.')], words_and_tags_list)


if __name__ == '__main__':
    unittest.main()

