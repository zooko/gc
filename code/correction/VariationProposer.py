# L. Amber Wilcox-O'Hearn 2013
# VariationProposer.py

class VariationProposer():

    def __init__(self, pos_tagger, tag_dictionary):
        self.pos_tagger = pos_tagger
        self.tag_dictionary = tag_dictionary


    def closed_class_alternatives(self, tokens):
        last_tag = self.pos_tagger(tokens)[-1] 
        if last_tag in ["IN", "DT"]:
            ind = self.tag_dictionary[last_tag].index(tokens[-1])
            return self.tag_dictionary[last_tag][:ind] + self.tag_dictionary[last_tag][ind+1:]
        else:
            return []
