# L. Amber Wilcox-O'Hearn 2013
# POSFiller.py

def fill_sentence(in_vocabulary_functions, pos_tagger_function, sentence):
    
    psos = pos_tagger_function(sentence)
    tokens = sentence.split()
    filled = []
    for i in range(len(in_vocabulary_functions)):
        filled.append([])
    for i in range(len(tokens)):
        for v in range(len(in_vocabulary_functions)):
            if in_vocabulary_functions[v](tokens[i]):
                filled[v].append(tokens[i])
            else:
                try:
                    filled[v].append(psos[i])
                except IndexError, e:
                    print sentence
                    print len(tokens), tokens
                    print len(psos), psos
                    raise e
    
    return filled
