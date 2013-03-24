# L. Amber Wilcox-O'Hearn 2011
# EssayRandomiser.py

# The CoNLL 2013 Shared Task Corpus includes a pre-processed set of
# essays.  See conllst13/CoNLL-preproc-README.

# This script will take a .conll and a corresponding .m2, and create
# two files, train.connl and devel.conll, containing approximately 80%
# and 20% respectively of the total text, in a random order, and
# corresponding train.m2 and devel.m2.

import sys, random

class Randomiser():
    def __init__(self, essay_file_obj, m2_file_obj, train_conll_file_obj, train_m2_file_obj, devel_conll_file_obj, devel_m2_file_obj, rand_obj):
        self.essay_file_obj = essay_file_obj
        self.m2_file_obj = m2_file_obj
        self.train_conll_file_obj = train_conll_file_obj
        self.train_m2_file_obj = train_m2_file_obj
        self.devel_conll_file_obj = devel_conll_file_obj
        self.devel_m2_file_obj = devel_m2_file_obj
        self.rand_obj = rand_obj

    def choose_outfiles(self):
        x = self.rand_obj.random()
        if x < .8: return self.train_conll_file_obj, self.train_m2_file_obj
        return self.devel_conll_file_obj, self.devel_m2_file_obj
        
    def randomise(self):
        current_id = ''
        for line in self.essay_file_obj:
            if line != '\n':
                essay_id = line.split()[0]
                if essay_id != current_id:
                    current_id = essay_id
                    outfiles = self.choose_outfiles()
            else:
                m2_line = self.m2_file_obj.readline()
                while m2_line and m2_line != '\n':
                    outfiles[1].write(m2_line)
                    m2_line = self.m2_file_obj.readline()
                outfiles[1].write(m2_line)
            outfiles[0].write(line)
        m2_line = self.m2_file_obj.readline()
        while m2_line and m2_line != '\n':
            outfiles[1].write(m2_line)
            m2_line = self.m2_file_obj.readline()
        outfiles[1].write(m2_line)


if __name__ == '__main__':
    essay_file_obj = sys.stdin
    train_conll_file_obj = open("train_conll", 'w')
    train_m2_file_obj = open("train_m2", 'w')
    devel_conll_file_obj = open("devel_conll", 'w')
    devel_m2_file_obj = open("devel_m2", 'w')
    r = random.Random(7)
    er = Randomiser(essay_file_obj, train_conll_file_obj, train_m2_file_obj, devel_conll_file_obj, devel_m2_file_obj, r)
    er.randomise()
