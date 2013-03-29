# L. Amber Wilcox-O'Hearn 2013
# POSFiller.py

def fill_sentence(in_vocabulary_function, pos_tagger_function, sentence):
    
    psos = pos_tagger_function(sentence)
    tokens = sentence.split()
    filled = []
    for i in range(len(tokens)):
        if in_vocabulary_function(tokens[i]):
            filled.append(tokens[i])
        else:
            filled.append(psos[i])
    
    return filled
