# L. Amber Wilcox-O'Hearn 2013
# GoldGenerator.py

# Takes the m2scorer formatted file and generates a file with one
# corrected sentence per line.

def correct_sentence(sentence, corrections):
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
    corrected += " ".join(tokens[index:])
    return " ".join(corrected.split()) + '\n'

def correct_file(m2_file_obj, gold_file_obj):
    corrections = []
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
            gold_file_obj.write(correct_sentence(sentence, corrections))
            corrections = []
            new_sentence = True

if __name__ == '__main__':
    import sys
    m2_file_obj = sys.stdin
    gold_file_obj = sys.stdout
    correct_file(m2_file_obj, gold_file_obj)
