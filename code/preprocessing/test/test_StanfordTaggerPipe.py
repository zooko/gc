# L. Amber Wilcox-O'Hearn 2013
# test_StanfordTaggerPipe.py

from code.preprocessing import StanfordTaggerPipe
import unittest

class StanfordTaggerPipeTest(unittest.TestCase):

    def setUp(self):

        stanford_tagger_path = 'stanford-tagger/stanford-postagger.jar:'
        module_path = 'edu.stanford.nlp.tagger.maxent.MaxentTagger'
        model_path = 'stanford-tagger/english-bidirectional-distsim.tagger'
        
        self.tagger_pipe = StanfordTaggerPipe.StanfordTaggerPipe(stanford_tagger_path, module_path, model_path)

    def test_stanford_tagger_pipe(self):

        self.tagger_pipe.stdin.write("Hello, World.\n")
        result = self.tagger_pipe.stdout.readline()
        self.assertEqual(result, "Hello_UH ,_, World_NNP ._.\n",  repr(result))
        result = self.tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

        self.tagger_pipe.stdin.write("Hello again, World.\n")
        result = self.tagger_pipe.stdout.readline()
        self.assertEqual(result, "Hello_UH again_RB ,_, World_NNP ._.\n",  repr(result))
        result = self.tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

        self.tagger_pipe.stdin.write("Hello, World.\n")
        result = self.tagger_pipe.stdout.readline()
        self.assertEqual(result, "Hello_UH ,_, World_NNP ._.\n",  repr(result))
        result = self.tagger_pipe.stdout.readline()
        self.assertEqual(result, '\n', repr(result))

    def test_tags_list(self):

        tags_list = self.tagger_pipe.tags_list("Hello, World.")
        self.assertEqual(tags_list, ["UH", ",", "NNP", "."], tags_list)
        tags_list = self.tagger_pipe.tags_list("Hello again, World.")
        self.assertEqual(tags_list, ["UH", "RB", ",", "NNP", "."], tags_list)
        tags_list = self.tagger_pipe.tags_list("Hello, World.")
        self.assertEqual(tags_list, ["UH", ",", "NNP", "."], tags_list)

    def test_words_and_tags_list(self):

        words_and_tags_list = self.tagger_pipe.words_and_tags_list("Hello, World.")
        self.assertEqual(words_and_tags_list, \
          [['Hello', 'UH'], [',', ','], ['World', 'NNP'], ['.', '.']], \
             words_and_tags_list)
        words_and_tags_list = self.tagger_pipe.words_and_tags_list("Hello again, World.")
        self.assertEqual(words_and_tags_list, \
          [['Hello', 'UH'], ['again', 'RB'], [',', ','], ['World', 'NNP'], ['.', '.']],  \
             words_and_tags_list)
        words_and_tags_list = self.tagger_pipe.words_and_tags_list("Hello, World.")
        self.assertEqual(words_and_tags_list, \
          [['Hello', 'UH'], [',', ','], ['World', 'NNP'], ['.', '.']],  \
             words_and_tags_list)

if __name__ == '__main__':
    unittest.main()

