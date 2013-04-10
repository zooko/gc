# L. Amber Wilcox-O'Hearn 2013
# VariationProposer.py

class VariationProposer():

    def __init__(self, pos_tagger, tag_dictionary, vocab_with_prefix):
        self.pos_tagger = pos_tagger
        self.tag_dictionary = tag_dictionary
        self.vocab_with_prefix = vocab_with_prefix


    def closed_class_alternatives(self, token, tag):

        ind = self.tag_dictionary[tag].index(token)
        return self.tag_dictionary[tag][:ind] + self.tag_dictionary[tag][ind+1:]

    def open_class_alternatives(self, token, tag_type):

        prefix = token[:-4]
        length = len(token)
        keys = [k for k in self.tag_dictionary.keys() if k.startswith(tag_type)]
        return [t for t in self.vocab_with_prefix(prefix) if len(t) <= length + 4 and reduce( lambda x,y: x or y, [t in self.tag_dictionary[k] for k in keys] ) ]

    def get_alternatives(self, token, tag):

        if tag in ["IN", "DT"]:
            return self.closed_class_alternatives(token, tag)
        if tag[:2] in ["NN", "VB"]:
            return self.open_class_alternatives(token, tag[:2])
        return []
