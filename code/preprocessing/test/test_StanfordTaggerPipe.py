# L. Amber Wilcox-O'Hearn 2013
# test_StanfordTaggerPipe.py

from code.preprocessing import StanfordTaggerPipe
import unittest

stanford_tagger_path = 'stanford-tagger/stanford-postagger.jar:'
module_path = 'edu.stanford.nlp.tagger.maxent.MaxentTagger'
model_path = 'stanford-tagger/english-bidirectional-distsim.tagger'

tagger_pipe = StanfordTaggerPipe.StanfordTaggerPipe(stanford_tagger_path, module_path, model_path)

class StanfordTaggerPipeTest(unittest.TestCase):

    def setUp(self):

        self.s0 = "Hello , World .\n"
        self.s1 = "Hello again, World.\n"
        self.s2 = "- { http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php } [ HYPERLINK : http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php ]\n"

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
        self.assertEqual(result, '-_: -LCB-_-LRB- http_NN :_: \/_: \/_: uci.edu\/features\/2009\/07\/feature_alzheimersstemcell_090720.php_NN -RCB-_-RRB- -LRB-_-LRB- HYPERLINK_NN :_: http_NN :_: \/_: \/_: uci.edu\/features\/2009\/07\/feature_alzheimersstemcell_090720.php_NN -RRB-_-RRB-\n',  repr(result))
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

    def test_tags_list(self):

        tags_list = tagger_pipe.tags_list(self.s0)
        self.assertEqual(tags_list, ['_UH', '_,', '_NNP', '_.'], tags_list)
        tags_list = tagger_pipe.tags_list(self.s1)
        self.assertEqual(tags_list, ['_UH', '_RB', '_,', '_NNP', '_.'], tags_list)
        tags_list = tagger_pipe.tags_list(self.s2)
        self.assertListEqual(tags_list, ['_:', '_-LRB-', '_NN', '_:', '_:', '_:', '_NN', '_-RRB-', '_-LRB-', '_NN', '_:', '_NN', '_:', '_:', '_:', '_NN', '_-RRB-'],  tags_list)

    def test_words_and_tags_list(self):

        words_and_tags_list = tagger_pipe.words_and_tags_list(self.s0)
        self.assertEqual(words_and_tags_list, \
          [('Hello', '_UH'), (',', '_,'), ('World', '_NNP'), ('.', '_.')], \
             words_and_tags_list)
        words_and_tags_list = tagger_pipe.words_and_tags_list(self.s1)
        self.assertEqual(words_and_tags_list, \
          [('Hello', '_UH'), ('again', '_RB'), (',', '_,'), ('World', '_NNP'), ('.', '_.')],  \
             words_and_tags_list)
        words_and_tags_list = tagger_pipe.words_and_tags_list(self.s2)
        self.assertListEqual(words_and_tags_list, \
             [('-', '_:'), ('-LCB-', '_-LRB-'), ('http', '_NN'), (':', '_:'), ('\\/', '_:'), ('\\/', '_:'), ('uci.edu\\/features\\/2009\\/07\\/feature_alzheimersstemcell_090720.php', '_NN'), ('-RCB-', '_-RRB-'), ('-LRB-', '_-LRB-'), ('HYPERLINK', '_NN'), (':', '_:'), ('http', '_NN'), (':', '_:'), ('\\/', '_:'), ('\\/', '_:'), ('uci.edu\\/features\\/2009\\/07\\/feature_alzheimersstemcell_090720.php', '_NN'), ('-RRB-', '_-RRB-')], \
             words_and_tags_list)

    def test_multi_sentence_line(self):
        
        multi_sentence = 'I am.  More than one.'
        tags_list = tagger_pipe.tags_list(multi_sentence)
        self.assertEqual(tags_list, ['_PRP', '_VBP', '_.', '_JJR', '_IN', '_CD', '_.'], tags_list)
        words_and_tags_list = tagger_pipe.words_and_tags_list(multi_sentence)
        self.assertListEqual(words_and_tags_list, \
             [('I', '_PRP'), ('am', '_VBP'), ('.', '_.'), ('More', '_JJR'), ('than', '_IN'), ('one', '_CD'), ('.', '_.')], \
             words_and_tags_list)


if __name__ == '__main__':
    unittest.main()

