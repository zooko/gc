# L. Amber Wilcox-O'Hearn 2011
# EssayRandomiser.py

# The CoNLL 2013 Shared Task Corpus includes a pre-processed set of
# essays.  See conllst13/CoNLL-preproc-README.

# This script will create two directories, train and  devel, containing
# approximately 80% and 20% respectively of the total text, in a random
# order.  

import sys, random

class Randomiser():
    def __init__(self, essay_file_obj, train_file_obj, devel_file_obj, rand_obj):
        self.essay_file_obj = essay_file_obj
        self.train_file_obj = train_file_obj
        self.devel_file_obj = devel_file_obj
        self.rand_obj = rand_obj

    def choose_outfile(self):
        x = self.rand_obj.random()
        if x < .8: return self.train_file_obj
        return self.devel_file_obj
        
    def randomise(self):
        current_id = ''
        for line in self.essay_file_obj:
            if line != '\n':
                essay_id = line.split()[0]
                if essay_id != current_id:
                    current_id = essay_id
                    outfile = self.choose_outfile()
            outfile.write(line)


if __name__ == '__main__':
    essay_file_obj = sys.stdin
    train_file_obj = open("train", 'w')
    devel_file_obj = open("devel", 'w')
    r = random.Random(7)
    er = Randomiser(essay_file_obj, train_file_obj, devel_file_obj, r)
    er.randomise()
