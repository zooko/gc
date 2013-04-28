# L. Amber Wilcox-O'Hearn 2013
# PrepareExternalCorpus.py

import sys, codecs, bz2, nltk, unicodedata

corpus_source_file_reader = codecs.getreader('utf-8')(sys.stdin, 'r')
segmented_and_tokenised_writer = codecs.getwriter('utf-8')(bz2.BZ2File('segmented_tokenised_corpus_section.bz2', 'w'))

text = corpus_source_file_reader.read()
assert isinstance(text, unicode)
assert len(text) > 0

trainer = nltk.tokenize.punkt.PunktTrainer()
trainer.ABBREV = .15
trainer.IGNORE_ABBREV_PENALTY = True
trainer.INCLUDE_ALL_COLLOCS = True
trainer.MIN_COLLOC_FREQ = 10
trainer.train(text)
sbd = nltk.tokenize.punkt.PunktSentenceTokenizer(trainer.get_params())


def is_an_initial(word):
    if len(word) == 2 and unicodedata.category(word[0])[0] == 'L' and word[1] == u'.':
        return True
    return False
def multi_char_word_and_starts_with_a_capital(word):
    if len(word) > 1 and unicodedata.category(word[0]) == 'Lu':
        return True
    return False

def apply_ugly_hack_to_reattach_wrong_splits_in_certain_cases_with_initials(lines):
    """
    NLTK currently splits sentences between 2 initials.  Hacking
    those back together.  Also has the effect of collapsing
    whitespace to a single space char.
    """
    lines = list(lines)
    if len(lines) == 0: return []
    reattached_lines = []
    i = 0
    current_line = lines[i].split()
    while i < len(lines) - 1:
        reattach = False
        next_line = lines[i+1].split()
        last_word = current_line[-1]
        next_line_starts_with_a_capital = False
        first_word_of_next_line = next_line[0]
        if len(first_word_of_next_line) > 1 and unicodedata.category(first_word_of_next_line[0]) == 'Lu':
            next_line_starts_with_a_capital = True
        if is_an_initial(last_word):
            nltk_ortho_context = sbd._params.ortho_context[first_word_of_next_line.lower()]
            if unicodedata.category(first_word_of_next_line[0])[0] != 'L':
                reattach = True
            # The following is an ugly and imperfect hack.  See mailing list for nltk.
            elif multi_char_word_and_starts_with_a_capital(first_word_of_next_line) and \
                    nltk_ortho_context <= 46 or \
                    is_an_initial(first_word_of_next_line):
                reattach = True

        if reattach:
                current_line += next_line
        else:
            reattached_lines.append(u' '.join(current_line))
            current_line = next_line
        i += 1 
    reattached_lines.append(u' '.join(current_line))
    return reattached_lines
            

for line in (t for t in text.split('\n')):
    sentences = sbd.sentences_from_text(line, realign_boundaries=True)
    sentences = apply_ugly_hack_to_reattach_wrong_splits_in_certain_cases_with_initials(sentences)
    for sentence in sentences:
        segmented_and_tokenised_writer.write(u' '.join(nltk.word_tokenize(sentence)) + u'\n')

