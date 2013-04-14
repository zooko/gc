# L. Amber Wilcox-O'Hearn 2013
# GoldGenerator.py

# Takes the m2scorer formatted file and generates a file with one
# corrected sentence per line.

import json

def correct_sentence_and_collect_insertables_and_deletables(sentence, corrections, insertables, deletables):
    tokens = sentence.split()[1:]
    span_substitions = []
    for line in corrections:
        correction_string_tokens = line.split('|||')
        indices = [int(x) for x in correction_string_tokens[0].split()[1:]]
        substitution_string = correction_string_tokens[2]
        span_substitions.append((indices, substitution_string))

    span_substitions.sort()
    corrected = ""
    index = 0
    for sub in span_substitions:
        corrected += " ".join(tokens[index:sub[0][0]]) + " " + sub[1] + " "
        index = sub[0][1]
        # Get insertables and deletables
        sub_tokens = sub[1].split()
        if len(sub_tokens) > sub[0][1] - sub[0][0]: # we have an inserted word
            original_tokens = tokens[sub[0][0]:sub[0][1]]
            for t in sub_tokens:
                if t not in original_tokens:
                    insertables.add(t.lower())
        if len(sub_tokens) < sub[0][1] - sub[0][0]: # we have a deleted word
            original_tokens = tokens[sub[0][0]:sub[0][1]]
            for t in original_tokens:
                if t not in sub_tokens:
                    deletables.add(t.lower())
    corrected += " ".join(tokens[index:])
    return " ".join(corrected.split()) + '\n'

def correct_file(m2_file_obj, gold_file_obj, ins_file_obj, del_file_obj):
    corrections = []
    insertables = set([])
    deletables = set([])
    new_sentence = True
    for line in m2_file_obj:
        if line.startswith("S "):
            assert new_sentence
            sentence = line
            new_sentence = False
        elif line.startswith("A "):
            assert not new_sentence
            corrections.append(line)
        else:
            assert line == '\n', line
            gold_file_obj.write(correct_sentence_and_collect_insertables_and_deletables(sentence, corrections, insertables, deletables))
            corrections = []
            new_sentence = True

    json.dump(list(insertables), ins_file_obj)
    json.dump(list(deletables), del_file_obj)

if __name__ == '__main__':
    import sys
    m2_file_obj = sys.stdin
    gold_file_obj = sys.stdout
    ins_file_obj = open(sys.argv[1], 'w')
    del_file_obj = open(sys.argv[2], 'w')
    correct_file(m2_file_obj, gold_file_obj, ins_file_obj, del_file_obj)
