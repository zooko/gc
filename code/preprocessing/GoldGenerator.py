# L. Amber Wilcox-O'Hearn 2013
# GoldGenerator.py

# Takes the m2scorer formatted file and generates a file with one
# corrected sentence per line.

class GoldGenerator():

    def __init__(self, m2_file_obj, gold_file_obj):
        self.m2_file_obj = m2_file_obj
        self.gold_file_obj = gold_file_obj

    def correct_sentence(self, sentence, corrections):
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
        return " ".join(corrected.split())
