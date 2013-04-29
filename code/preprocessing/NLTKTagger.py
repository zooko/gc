import nltk

class NLTKTagger:
    def words_and_tags_list(self, line):
        return nltk.pos_tag(line.strip().split())
