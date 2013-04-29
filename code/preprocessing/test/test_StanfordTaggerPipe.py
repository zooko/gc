# L. Amber Wilcox-O'Hearn 2013
# test_StanfordTaggerPipe.py

from code.preprocessing import StanfordTaggerPipe
import unittest

stanford_tagger_path = 'stanford-tagger/stanford-postagger.jar:'
module_path = 'edu.stanford.nlp.tagger.maxent.MaxentTagger'
model_path = 'stanford-tagger/models/english-bidirectional-distsim.tagger'

tagger_pipe = StanfordTaggerPipe.StanfordTaggerPipe(stanford_tagger_path, module_path, model_path)

class StanfordTaggerPipeTest(unittest.TestCase):

    def setUp(self):

        self.s0 = u"Hello , World .\n"
        self.s1 = u"Hello again , World .\n"
        self.s2 = u"- { http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php } [ HYPERLINK : http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php ]\n"
        self.s3 = u"Hence the RTI system is very inexpensively and can be commonly used ( Retinal Technologies , Inc. Launches Company and Revolutionizes Biometrics With Patented Retinal Scanning Technology , 2001 ) ."

    def test_stanford_tagger_pipe(self):

        tagger_pipe.stdin_byte_writer.write(self.s0)
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, 'Hello_UH ,_, World_NNP ._.\n',  repr(result))
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

        tagger_pipe.stdin_byte_writer.write(self.s1)
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, 'Hello_UH again_RB ,_, World_NNP ._.\n',  repr(result))
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

        tagger_pipe.stdin_byte_writer.write(self.s2)
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, "-_: {_FW http_FW :_: //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php_FW }_FW [_FW HYPERLINK_NN :_: http_NN :_: //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php_FW ]_FW\n",  repr(result))
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

    def test_tags_list(self):

        tags_list = tagger_pipe.tags_list(self.s0)
        self.assertEqual(tags_list, ['UH', ',', 'NNP', '.'], tags_list)
        tags_list = tagger_pipe.tags_list(self.s1)
        self.assertEqual(tags_list, ['UH', 'RB', ',', 'NNP', '.'], tags_list)
        tags_list = tagger_pipe.tags_list(self.s2)
        self.assertListEqual(tags_list, [':', '-LRB-', 'JJ', ':', 'NN', '-RRB-', '-LRB-', 'NN', ':', 'NN', ':', 'NN', '-RRB-'], tags_list)
        for i in tags_list:
            self.assertIsInstance(i, unicode, i)

    def test_words_and_tags_list(self):

        words_and_tags_list = tagger_pipe.words_and_tags_list(self.s0)
        self.assertEqual(words_and_tags_list, \
          [('Hello', 'UH'), (',', ','), ('World', 'NNP'), ('.', '.')], \
             words_and_tags_list)
        words_and_tags_list = tagger_pipe.words_and_tags_list(self.s1)
        self.assertEqual(words_and_tags_list, \
          [('Hello', 'UH'), ('again', 'RB'), (',', ','), ('World', 'NNP'), ('.', '.')],  \
             words_and_tags_list)
        words_and_tags_list = tagger_pipe.words_and_tags_list(self.s2)
        self.assertListEqual(words_and_tags_list, \
             [('-', ':'), ('-LRB-', '-LRB-'), ('http', 'JJ'), (':', ':'), ('//uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php', 'NN'), ('-RRB-', '-RRB-'), ('-LRB-', '-LRB-'), ('HYPERLINK', 'NN'), (':', ':'), ('http', 'NN'), (':', ':'), ('//uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php', 'NN'), ('-RRB-', '-RRB-')], \
             words_and_tags_list)

    def test_multi_sentence_line(self):
        multi_sentence = u'I am .  More than one .\n'
        tags_list = tagger_pipe.tags_list(multi_sentence)
        self.assertEqual(tags_list, ['PRP', 'VBP', '.', 'JJR', 'IN', 'CD', '.'], tags_list)
        words_and_tags_list = tagger_pipe.words_and_tags_list(multi_sentence)
        self.assertListEqual(words_and_tags_list, \
             [('I', 'PRP'), ('am', 'VBP'), ('.', '.'), ('More', 'JJR'), ('than', 'IN'), ('one', 'CD'), ('.', '.')], \
             words_and_tags_list)
        for i in words_and_tags_list:
            self.assertIsInstance(i[0], unicode, i)
            self.assertIsInstance(i[1], unicode, i)

    def test_unicode(self):
        self.skipTest('')
        unicode_sentence = '496e204275726d6573652063756973696e65202c2061207377656574206a656c6c79206b6e6f776e2061732022206b7961756b206b7961772022202820e2808b20e180b120e1808020e180bb20e180ac20e1808020e180ba20e2808b20e180b120e1808020e180bc20e180ac205b207420ca8320616f20ca94207420ca83206175205d2029206973206d6164652066726f6d2061676172202e0a'.decode('hex').decode('utf-8')
        words_and_tags_list = tagger_pipe.words_and_tags_list(unicode_sentence)
        self.assertListEqual(words_and_tags_list, [], words_and_tags_list)


if __name__ == '__main__':
    unittest.main()

