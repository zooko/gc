# L. Amber Wilcox-O'Hearn 2012
# SConstruct

# Ugly hack to avoid problem caused by ugly hack.
# See http://scons.tigris.org/issues/show_bug.cgi?id=2781
import sys
del sys.modules['pickle']

import codecs, bz2, gzip, random, subprocess, os, StringIO, filecmp

from code.preprocessing import EssayRandomiser, GoldGenerator
from code.language_modelling import VocabularyCutter

def open_with_unicode(file_name, compression_type, mode):
    assert compression_type in [None, 'gzip', 'bzip2']
    assert mode in ['r', 'w']
    if compression_type == None:
        if mode == 'r':
            return codecs.getreader('utf-8')(open(file_name, mode))
        elif mode == 'w':
            return codecs.getwriter('utf-8')(open(file_name, mode))
    elif compression_type == 'gzip':
        if mode == 'r':
            return codecs.getreader('utf-8')(gzip.GzipFile(file_name, mode))
        elif mode == 'w':
            return codecs.getwriter('utf-8')(gzip.GzipFile(file_name, mode))
    elif compression_type == 'bzip2':
        if mode == 'r':
            return codecs.getreader('utf-8')(bz2.BZ2File(file_name, mode))
        elif mode == 'w':
            return codecs.getwriter('utf-8')(bz2.BZ2File(file_name, mode))

def randomise_essays(target, source, env):
    """
    target is a list of files corresponding to the training and
    development sets.  source is a single file of essays.
    """
    essay_file_obj = open_with_unicode(source[0].path, None, 'r')
    m2_file_obj = open_with_unicode(source[1].path, None, 'r')
    m2_5_file_obj = open_with_unicode(source[2].path, None, 'r')
    train_conll_file_obj = open_with_unicode(target[0].path, None, 'w')
    train_m2_file_obj = open_with_unicode(target[1].path, None, 'w')
    train_m2_5_file_obj = open_with_unicode(target[2].path, None, 'w')
    devel_conll_file_obj = open_with_unicode(target[3].path, None, 'w')
    devel_m2_file_obj = open_with_unicode(target[4].path, None, 'w')
    devel_m2_5_file_obj = open_with_unicode(target[5].path, None, 'w')
    rand_obj = random.Random(7)
    er = EssayRandomiser.Randomiser(essay_file_obj, m2_file_obj, m2_5_file_obj, train_conll_file_obj, train_m2_file_obj, train_m2_5_file_obj, devel_conll_file_obj, devel_m2_file_obj, devel_m2_5_file_obj, rand_obj)
    er.randomise()
    return None

def training_m2_5_to_gold(target, source, env):
     """
     """
     train_m2_5_file_obj = open_with_unicode(source[0].path, None, 'r')
     train_gold_file_obj = open_with_unicode(target[0].path, None, 'w')
     GoldGenerator.correct_file(train_m2_5_file_obj, train_gold_file_obj)
     return None


def create_vocabularies(target, source, env):
    """
    """
    train_gold_file_name = source[0].path
    srilm_ngram_counts = subprocess.Popen(['ngram-count', '-order', '1', '-tolower', '-text', train_gold_file_name, '-sort', '-write', data_directory + 'counts'])
    srilm_ngram_counts.wait()

    if all_vocabulary_sizes:
        unigram_counts_file_obj = open_with_unicode(data_directory + 'counts', None, 'r')
        size = all_vocabulary_sizes[0]
        vocabulary_file_name = data_directory + str(size) + 'K.vocab'
        assert target[0].path == vocabulary_file_name, 'Target was: ' + target[0].path + '; Expected: ' + vocabulary_file_name
        vocabulary_file_obj = open_with_unicode(vocabulary_file_name, None, 'w')
        cutter = VocabularyCutter.VocabularyCutter(unigram_counts_file_obj, vocabulary_file_obj)
        cutter.cut_vocabulary(int(float(size)*1000))
        vocabulary_file_obj.close()
        base_vocabulary_file_obj = open_with_unicode(vocabulary_file_name, None, 'r')
        base_vocabulary = base_vocabulary_file_obj.readlines()

        for i in range(len(all_vocabulary_sizes))[1:]:
            size = all_vocabulary_sizes[i]
            vocabulary_file_name = data_directory + str(size) + 'K.vocab'
            assert target[i].path == vocabulary_file_name, 'Target was: ' + target[i].path + '; Expected: ' + vocabulary_file_name
            vocabulary_file_obj = open_with_unicode(vocabulary_file_name, None, 'w')
            for line in base_vocabulary[:int(float(size)*1000)]:
                vocabulary_file_obj.write(line)
    return None

def create_trigram_models(target, source, env):

    train_gold_file_name = source[0].path

    for i in range(len(vocabulary_sizes)):
        size = vocabulary_sizes[i]
        vocabulary_file_name = data_directory + str(size) + 'K.vocab'
        trigram_model_name = data_directory + 'trigram_model_' + str(size) + 'K.arpa'
        assert target[i].path == trigram_model_name, target[i].path
        srilm_make_lm = subprocess.Popen(['ngram-count', '-vocab', vocabulary_file_name, '-tolower', '-unk', '-kndiscount3', '-debug', '2', '-text', train_gold_file_name, '-lm', trigram_model_name])
        srilm_make_lm.wait()

    return None

# Get commandline configuration:

data_directory = ''
vocabulary_sizes = []
pos_vocabulary_sizes = []
TEST = False

try:
    data_directory = [x[1] for x in ARGLIST if x[0] == "data_directory"][0] + '/'
except:
    print "Usage: scons data_directory=DIR variables target"
    raise Exception

if [x for x in ARGLIST if x[0] == "test"]:
    TEST = True
    vocabulary_sizes = [0.1, 0.5]
    pos_vocabulary_sizes = [0.05]
else:
    for key, value in ARGLIST:
        if key == "vocabulary_size":
            vocabulary_sizes.append(value)
        elif key == "pos_vocabulary_size":
            pos_vocabulary_sizes.append(value)

all_vocabulary_sizes = list(set(vocabulary_sizes)|set(pos_vocabulary_sizes))
all_vocabulary_sizes.sort(reverse=True)

print vocabulary_sizes, pos_vocabulary_sizes, all_vocabulary_sizes

learning_sets_builder = Builder(action = randomise_essays)
training_gold_builder = Builder(action = training_m2_5_to_gold)
vocabulary_files_builder = Builder(action = create_vocabularies)
trigram_models_builder = Builder(action = create_trigram_models)

env = Environment(BUILDERS = {'learning_sets' : learning_sets_builder, 'training_gold': training_gold_builder, 'vocabulary_files': vocabulary_files_builder, 'trigram_models' : trigram_models_builder})

env.learning_sets([data_directory + set_name for set_name in ['training_set', 'training_set_m2', 'training_set_m2_5', 'development_set', 'development_set_m2', 'development_set_m2_5']], [data_directory + 'corpus', data_directory + 'm2', data_directory + 'm2_5'])

env.Alias('learning_sets', [data_directory + set_name for set_name in ['training_set', 'training_set_m2', 'training_set_m2_5', 'development_set', 'development_set_m2', 'development_set_m2_5']])

env.training_gold([data_directory + 'training_set_gold'], [data_directory + 'training_set_m2_5'])
 
env.Alias('training_gold', data_directory + 'training_set_gold')

env.vocabulary_files([data_directory + str(size) + 'K.vocab' for size in all_vocabulary_sizes], [data_directory + 'training_set_gold'])

env.Alias('vocabulary_files', [data_directory + str(size) + 'K.vocab' for size in all_vocabulary_sizes])

env.trigram_models([data_directory + 'trigram_model_' + str(size) + 'K.arpa' for size in vocabulary_sizes], [data_directory + 'training_set_gold'] + [data_directory + str(size) + 'K.vocab' for size in vocabulary_sizes])

env.Alias('trigram_models', [data_directory + 'trigram_model_' + str(size) + 'K.arpa' for size in vocabulary_sizes])
