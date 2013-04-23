# L. Amber Wilcox-O'Hearn 2013
# VariationProposer.py

from collections import OrderedDict
from nltk.stem import PorterStemmer

class VariationProposer():

    def __init__(self, tag_dictionary, tmpipe_obj, insertables, deletables):
        self.vocab_with_prefix = tmpipe_obj.vocabulary_with_prefix
        self.tag_dictionary = tag_dictionary
        self.AUX = {'are': 'VBP',
               'be': 'VB',
               'been': 'VBN',
               'being': 'VBG',
               'did': 'VBD',
               'do': 'VB',
               'does': 'VBZ',
               'get': 'VB',
               'getting': 'VBG',
               'got': 'VBD',
               'had': 'VBD',
               'has': 'VBZ',
               'have': 'VB',
               'having': 'VBG',
               'is': 'VBZ',
               'was': 'VBD',
               'were': 'VBD'}
        closed_class_tags = ['IN', 'DT', 'TO', 'MD']
        self.closed_class_preceder_tokens = set([])
        for token in [i for i in insertables if tmpipe_obj.in_vocabulary(i)]:
            for tag in closed_class_tags:
                if token in tag_dictionary[tag]:
                    self.closed_class_preceder_tokens.add((token, tag))
                elif token in self.AUX.keys():
                    self.closed_class_preceder_tokens.add((token, self.AUX[token]))
        self.closed_class_deletables = set([])
        for token in [d for d in deletables if tmpipe_obj.in_vocabulary(d)]:
            for tag in closed_class_tags:
                if token in tag_dictionary[tag]:
                    self.closed_class_deletables.add((token, tag))
                elif token in self.AUX.keys():
                    self.closed_class_deletables.add((token, self.AUX[token]))
        self.tmpipe_obj = tmpipe_obj
        self.cache = OrderedDict()
        self.cache_size = 500
        self.cache_stats = [0,0]
        self.stemmer = PorterStemmer()

    def closed_class_alternatives(self, token, tag):

        if tag == 'AUX':
            alternatives = [(k,v) for k,v in self.AUX.iteritems() if k != token and self.tmpipe_obj.in_vocabulary(k)]
        else:
            alternatives = [(alt, tag) for alt in self.tag_dictionary[tag] if alt != token and self.tmpipe_obj.in_vocabulary(alt)]

        if (token, tag) in self.closed_class_deletables:
            alternatives.append(())

        return set(alternatives)

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

    def open_class_alternatives(self, token, tag):
        
        tag_type = tag[:2]

        if len(token) > 4:
            prefix = token[:-4]
            suffix = token[-4:]
        else:
            prefix = token[0]
            suffix = token[1:]
#        prefix_tokens = [t for t in self.vocab_with_prefix(prefix) if self.levenshtein_distance(suffix, t[len(prefix):]) <= 4]
        prefix_tokens = [t for t in self.vocab_with_prefix(prefix) if self.stemmer.stem(t) == self.stemmer.stem(token)]

        relevant_tag_prefix_tokens_with_tag = set([])
        if tag_type == 'VB':
            keys = [k for k in self.tag_dictionary.keys() if k.startswith(tag_type) and k != tag]
        else:
            assert tag_type == 'NN', tag_type
            if tag == 'NNS' and 'NN' in self.tag_dictionary.keys():
                keys = ['NN']
            elif tag == 'NN' and 'NNS' in self.tag_dictionary.keys():
                keys = ['NNS']
            elif tag == 'NNPS' and 'NNP' in self.tag_dictionary.keys():
                keys = ['NNP']
            elif tag == 'NNP' and 'NNPS' in self.tag_dictionary.keys():
                keys = ['NNPS']
            else:
                assert False, tag

        for pt in prefix_tokens:
            for k in keys:
                if pt in self.tag_dictionary[k]:
                    relevant_tag_prefix_tokens_with_tag.add((pt, k))
                    break
        if (token, tag) in relevant_tag_prefix_tokens_with_tag:
            relevant_tag_prefix_tokens_with_tag.remove((token, tag))
        return relevant_tag_prefix_tokens_with_tag

    def get_alternatives(self, token, tag):

        if self.cache.has_key( (token, tag) ):
            self.cache_stats[0] += 1
            alternatives = self.cache[(token, tag)]
            del(self.cache[(token, tag)])
            self.cache[(token, tag)] = alternatives
            return alternatives

        self.cache_stats[1] += 1
        if tag in ["IN", "DT"]:
            alternatives = self.closed_class_alternatives(token, tag)
        elif token in self.AUX.keys():
            alternatives = self.closed_class_alternatives(token, 'AUX')
        elif tag[:2] in ["NN", "VB"]:
            alternatives = self.open_class_alternatives(token, tag)
        else:
            alternatives = set([])

#        print "Token, tag, alternatives: ", token, tag, alternatives
        self.cache[(token, tag)] = alternatives
        if len(self.cache) > self.cache_size:
            self.cache.popitem(last=False)

        return alternatives

    def generate_path_variations(self, tagged_sentence):

        path_variations = []

        last_token = tagged_sentence[-1][0]
        last_tag = tagged_sentence[-1][1]

        '''
        Do upper first, for 'I'.  Then it will be restored even if
        not at the beginning of a sentence.
        '''
        if last_token.isupper():
            case = 'u'
        elif last_token.istitle():
            case = 't'
        else:
            case = None

        token_variations = self.get_alternatives(last_token.lower(), last_tag)

        for var in token_variations:

            if var == ():
                # Deletion
                path_variations.append(tagged_sentence[:-1])

            else:
                '''
                Do upper first, for 'I'.  Then it will be restored even if
                not at the beginning of a sentence.
                '''
                if case == 'u':
                    recased_var = (var[0].upper(), var[1])
                elif case == 't':
                    recased_var = (var[0].title(), var[1])
                else:
                    recased_var = var

                # Substitution and no insertion
                path_variations.append(tagged_sentence[:-1] + [recased_var])

                for insertion_token in self.closed_class_preceder_tokens:

                    if len(tagged_sentence) == 1: # Substitution and insertion at beginning.
                        insertion_token = (insertion_token[0].title(), insertion_token[1])
                        if case != 't' and var[0] != 'a':
                            path_variations.append(tagged_sentence[:-1] + [insertion_token] + [recased_var])
                        else:
                            path_variations.append(tagged_sentence[:-1] + [insertion_token] + [var])

                    else:
                        # Substitution and insertion not at beginning
                        path_variations.append(tagged_sentence[:-1] + [insertion_token] + [recased_var])

        for insertion_token in self.closed_class_preceder_tokens:

            possibly_recased_token = tagged_sentence[-1]

            # Insertion with no deletion or substitution
            if len(tagged_sentence) == 1:
                insertion_token = (insertion_token[0].title(), insertion_token[1])
                if case == 't':
                    possibly_recased_token = (last_token.lower(), last_tag)

            path_variations.append(tagged_sentence[:-1] + [insertion_token] + [possibly_recased_token])
        return path_variations

    def print_cache_stats(self):

        print "Cache hits:", self.cache_stats[0]
        print "Cache misses:", self.cache_stats[1]
