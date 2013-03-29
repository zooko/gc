# L. Amber Wilcox-O'Hearn 2013
# test_StanfordTaggerPipe.py

from code.preprocessing import StanfordTaggerPipe
import unittest

stanford_tagger_path = 'stanford-tagger/stanford-postagger.jar:'
module_path = 'edu.stanford.nlp.tagger.maxent.MaxentTagger'
model_path = 'stanford-tagger/english-bidirectional-distsim.tagger'

tagger_pipe = StanfordTaggerPipe.StanfordTaggerPipe(stanford_tagger_path, module_path, model_path)

class StanfordTaggerPipeTest(unittest.TestCase):

    def test_stanford_tagger_pipe(self):

        tagger_pipe.stdin_byte_writer.write("Hello, World.\n")
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, "Hello_UH ,_, World_NNP ._.\n",  repr(result))
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

        tagger_pipe.stdin_byte_writer.write("Hello again, World.\n")
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, "Hello_UH again_RB ,_, World_NNP ._.\n",  repr(result))
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

        tagger_pipe.stdin_byte_writer.write("- { http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php } [ HYPERLINK : http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php ]\n")
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, "-_: -LCB-_-LRB- http_NN :_: \/_: \/_: uci.edu\/features\/2009\/07\/feature_alzheimersstemcell_090720.php_NN -RCB-_-RRB- -LRB-_-LRB- HYPERLINK_NN :_: http_NN :_: \/_: \/_: uci.edu\/features\/2009\/07\/feature_alzheimersstemcell_090720.php_NN -RRB-_-RRB-\n",  repr(result))
        result = tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

    def test_tags_list(self):

        tags_list = tagger_pipe.tags_list("Hello, World.")
        self.assertEqual(tags_list, ["UH", ",", "NNP", "."], tags_list)
        tags_list = tagger_pipe.tags_list("Hello again, World.")
        self.assertEqual(tags_list, ["UH", "RB", ",", "NNP", "."], tags_list)
        tags_list = tagger_pipe.tags_list("- { http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php } [ HYPERLINK : http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php ]\n")
        self.assertListEqual(tags_list, [":", "-LRB-", "NN", ":", ":", ":", "NN", "-RRB-", "-LRB-", "NN", ":", "NN", ":", ":", ":", "NN", "-RRB-"],  tags_list)

    def test_words_and_tags_list(self):

        words_and_tags_list = tagger_pipe.words_and_tags_list("Hello, World.")
        self.assertEqual(words_and_tags_list, \
          [('Hello', 'UH'), (',', ','), ('World', 'NNP'), ('.', '.')], \
             words_and_tags_list)
        words_and_tags_list = tagger_pipe.words_and_tags_list("Hello again, World.")
        self.assertEqual(words_and_tags_list, \
          [('Hello', 'UH'), ('again', 'RB'), (',', ','), ('World', 'NNP'), ('.', '.')],  \
             words_and_tags_list)
        words_and_tags_list = tagger_pipe.words_and_tags_list("- { http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php } [ HYPERLINK : http : //uci.edu/features/2009/07/feature_alzheimersstemcell_090720.php ]\n")
        self.assertListEqual(words_and_tags_list, \
             [('-', ':'), ('-LCB-', '-LRB-'), ('http', 'NN'), (':', ':'), ('\\/', ':'), ('\\/', ':'), ('uci.edu\\/features\\/2009\\/07\\/feature_alzheimersstemcell_090720.php', 'NN'), ('-RCB-', '-RRB-'), ('-LRB-', '-LRB-'), ('HYPERLINK', 'NN'), (':', ':'), ('http', 'NN'), (':', ':'), ('\\/', ':'), ('\\/', ':'), ('uci.edu\\/features\\/2009\\/07\\/feature_alzheimersstemcell_090720.php', 'NN'), ('-RRB-', '-RRB-')], \
             words_and_tags_list)

    def test_multi_sentence_line(self):
        
        multi_sentence = "I am.  More than one."
        tags_list = tagger_pipe.tags_list(multi_sentence)
        self.assertEqual(tags_list, ["PRP", "VBP", ".", "JJR", "IN", "CD", "."], tags_list)
        words_and_tags_list = tagger_pipe.words_and_tags_list(multi_sentence)
        self.assertListEqual(words_and_tags_list, \
             [('I', "PRP"), ('am', "VBP"), ('.', "."), ('More', "JJR"), ('than', "IN"), ('one', "CD"), ('.', ".")], \
             words_and_tags_list)


if __name__ == '__main__':
    unittest.main()

