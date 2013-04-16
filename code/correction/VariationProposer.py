# L. Amber Wilcox-O'Hearn 2013
# VariationProposer.py

class VariationProposer():

    def __init__(self, pos_tagger, tag_dictionary, vocab_with_prefix, insertables):
        self.pos_tagger = pos_tagger
        self.vocab_with_prefix = vocab_with_prefix
        self.tag_dictionary = tag_dictionary
        self.tag_dictionary['AUX'] = ['be', 'is', 'are', 'were', 'was', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'get', 'got', 'getting']
        closed_class_preceder_tags = ['IN', 'DT', 'TO', 'MD', 'AUX']
        self.closed_class_preceder_tokens = set([])
        for token in insertables:
            for tag in closed_class_preceder_tags:
                if token in tag_dictionary[tag]:
                    self.closed_class_preceder_tokens.add(token)

    def closed_class_alternatives(self, token, tag):

        try:
            ind = self.tag_dictionary[tag].index(token)
            return self.tag_dictionary[tag][:ind] + self.tag_dictionary[tag][ind+1:]
        except ValueError:
            return self.tag_dictionary[tag]

    def levenshtein_distance(self, seq1, seq2):
        one_ago = None
        this_row = range(1, len(seq2) + 1) + [0]
        for x in xrange(len(seq1)):
            two_ago, one_ago, this_row = one_ago, this_row, [0] * len(seq2) + [x + 1]
            for y in xrange(len(seq2)):
                del_cost = one_ago[y] + 1
                add_cost = this_row[y - 1] + 1
                sub_cost = one_ago[y - 1] + (seq1[x] != seq2[y])
                this_row[y] = min(del_cost, add_cost, sub_cost)
        return this_row[len(seq2) - 1]

    def open_class_alternatives(self, token, tag_type):

        if len(token) > 4:
            prefix = token[:-4]
            suffix = token[-4:]
        else:
            prefix = token[0]
            suffix = token[1:]
        prefix_tokens = [t for t in self.vocab_with_prefix(prefix) if self.levenshtein_distance(suffix, t[len(prefix):]) <= 4]
        relevant_tag_prefix_tokens = []
        keys = [k for k in self.tag_dictionary.keys() if k.startswith(tag_type)]
        for pt in prefix_tokens:
            for k in keys:
                if pt in self.tag_dictionary[k]:
                    relevant_tag_prefix_tokens.append(pt)
                    break
        return relevant_tag_prefix_tokens

    def get_alternatives(self, token, tag):

        if tag in ["IN", "DT", "AUX"]:
            return self.closed_class_alternatives(token, tag)
        if tag[:2] in ["NN", "VB"]:
            return self.open_class_alternatives(token, tag[:2])
        return []

    def generate_path_variations(self, sentence):

        path_variations = []
        tags = self.pos_tagger(sentence)
        tokens = sentence.split()
        token_variations = self.get_alternatives(tokens[-1], tags[-1])
        for var in token_variations:
            if var == '':
                path_variations.append(tokens[:-1])
            else:
                path_variations.append(tokens[:-1] + [var])
                for insertion_token in self.closed_class_preceder_tokens:
                    path_variations.append(tokens[:-1] + [insertion_token] + [var])
        for insertion_token in self.closed_class_preceder_tokens:
            path_variations.append(tokens[:-1] + [insertion_token] + [tokens[-1]])
        return path_variations
