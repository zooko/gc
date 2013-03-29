# L. Amber Wilcox-O'Hearn 2013
# StanfordTaggerPipe.py

import os, subprocess

class StanfordTaggerPipe:
    def __init__(self, stanford_tagger_path, module_path, model_path):
        self.tagger_pipe = subprocess.Popen(['java', '-mx1g', '-cp', stanford_tagger_path, module_path, '-model', model_path ], stdin=-1, stdout=-1)
        self.stdin = self.tagger_pipe.stdin
        self.stdout = self.tagger_pipe.stdout

    def tags_list(self, token_string):
        self.tagger_pipe.stdin.write(token_string + '\n')
        result = self.tagger_pipe.stdout.readline()
        newline = self.tagger_pipe.stdout.readline()
        assert(newline == '\n'), repr(newline)
        return [y[1] for y in [x.split('_') for x in result.split()]]

    def shutdown(self):
        if hasattr(self, "tagger_pipe"):
            if hasattr(self.tagger_pipe, "pid") and self.tagger_pipe.pid:
                os.kill(self.tagger_pipe.pid, 15)
            self.tagger_pipe.wait()

    def __del__(self):
        self.shutdown()
