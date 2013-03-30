# L. Amber Wilcox-O'Hearn 2013
# StanfordTaggerPipe.py

import os, subprocess, codecs

class StanfordTaggerPipe:
    def __init__(self, stanford_tagger_path, module_path, model_path):
        self.tagger_pipe = subprocess.Popen(['java', '-mx1g', '-cp', stanford_tagger_path, module_path, '-model', model_path, '-tokenize', 'false' ], stdin=-1, stdout=-1)
        self.stdin_byte_writer = codecs.getwriter('utf-8')(self.tagger_pipe.stdin)
        self.stdout = self.tagger_pipe.stdout

    def tokenise_parentheses(self, sentence):
        '''
        We are assuming the string has already been tokenised, and so
        we do not want the tagger to tokenise again.  However, the
        tagger has special tokens for parentheses needed for good
        performance.  Here we translate those.
        '''
        left_parentheses = '{[('
        right_parentheses = '}])'
        for lp in left_parentheses: sentence = sentence.replace(lp, "-LRB-")
        for rp in right_parentheses: sentence = sentence.replace(rp, "-RRB-")
        return sentence

    def tags_list(self, token_string):
        self.stdin_byte_writer.write(self.tokenise_parentheses(token_string) + '\n')
        result = self.tagger_pipe.stdout.readline()
        newline = self.tagger_pipe.stdout.readline()
        assert(newline == '\n'), repr(newline)

        # The following is to take care of (most) cases when the
        # tagger believes there is more than one sentence on a line.
        # Since my program can't know in general how much output to
        # expect, and can't just wait in case of more, I am counting
        # tokens, and trying for another line if there don't seem to
        # be enough.

#        tokens = token_string.split()
        result_tokens = result.split()
#        while len(result_tokens) < len(tokens):
#            result = self.tagger_pipe.stdout.readline()
#            newline = self.tagger_pipe.stdout.readline()
#            assert(newline == '\n'), repr(newline)
#            result_tokens += result.split()
        return ['_' + y[-1] for y in [x.rpartition('_') for x in result_tokens]]

    def words_and_tags_list(self, token_string):
        self.stdin_byte_writer.write(self.tokenise_parentheses(token_string) + '\n')
        result = self.tagger_pipe.stdout.readline()
        newline = self.tagger_pipe.stdout.readline()
        assert(newline == '\n'), repr(newline)
#        tokens = token_string.split()
        result_tokens = result.split()

        # See comment in tags_list
#        while len(result_tokens) < len(tokens):
#            result = self.tagger_pipe.stdout.readline()
#            newline = self.tagger_pipe.stdout.readline()
#            assert(newline == '\n'), repr(newline)
#            result_tokens += result.split()

        return [(y[0], '_' + y[-1]) for y in [x.rpartition('_') for x in result_tokens]]

    def shutdown(self):
        if hasattr(self, "tagger_pipe"):
            if hasattr(self.tagger_pipe, "pid") and self.tagger_pipe.pid:
                os.kill(self.tagger_pipe.pid, 15)
            self.tagger_pipe.wait()

    def __del__(self):
        self.shutdown()
