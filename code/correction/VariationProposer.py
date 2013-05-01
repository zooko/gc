# L. Amber Wilcox-O'Hearn 2013
# VariationProposer.py

from collections import OrderedDict, defaultdict, Counter
from nltk.stem import PorterStemmer
from math import log10

N = 5 # We will use the top N most frequent words in each closed class.
closed_class_tags = ['IN', 'DT', 'MD']
AUX = {'are': 'VBP',
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

class VariationProposer():

    def __init__(self, tag_dictionary, tmpipe_obj):
        self.tmpipe_obj = tmpipe_obj
        self.vocab_with_prefix = tmpipe_obj.vocabulary_with_prefix

        # key: stanford tag, value: list of tokens that were found in
        # the training data
        self.tag_dictionary = defaultdict(list)

        # Transform the count_dict inside tag_dictionary to just a
        # list of tokens.
        for tag, token_count_dict in tag_dictionary.iteritems():
            self.tag_dictionary[tag] = token_count_dict.keys()

        # key: amber tag, value: limited list of token, stanford tag
        # tuples (the top N plus maybe a couple more).
        self.closed_class_substitutables = {}

        for tag in closed_class_tags:
            counter = Counter(tag_dictionary[tag])
            self.closed_class_substitutables[tag] = [(token,tag) for token in [x[0] for x in counter.most_common(N)] if tmpipe_obj.in_vocabulary(token)]

        aux_counts = []
        for token,tag in AUX.iteritems():
            if tmpipe_obj.in_vocabulary(token) and token in tag_dictionary[tag]:
                aux_counts.append( (tag_dictionary[tag][token], (token, tag) ))
        aux_counts.sort()
        self.closed_class_substitutables['AUX'] = [ a[1] for a in aux_counts[-N:] ]

        self.closed_class_substitutables['IN'].append( ('to', 'TO') )
        self.closed_class_substitutables['AUX'].append( ('to', 'TO') )

        # Let () represent the empty substitution
        for tag in self.closed_class_substitutables.keys():
            self.closed_class_substitutables[tag].append(())

        # insertables is the set of all token, tag tuple in closed_class_substitutables
        self.closed_class_insertables = set()
        for token_tag_list in self.closed_class_substitutables.itervalues():
            self.closed_class_insertables |= set(token_tag_list)
        self.closed_class_insertables.discard(())

        self.cache = OrderedDict()
        self.cache_size = 500
        self.cache_stats = [0,0]
        self.stemmer = PorterStemmer()

    def closed_class_alternatives(self, token, tag):

        return set(self.closed_class_substitutables[tag]) - set([(token, tag)])

    def open_class_alternatives(self, token, tag):

        tag_type = tag[:2]

        if tag_type == 'VB':
            keys = sorted([k for k in self.tag_dictionary if k.startswith(tag_type) and k != tag])
        else:
            assert tag_type == 'NN', tag_type
            if tag == 'NNS' and 'NN' in self.tag_dictionary:
                keys = ['NN']
            elif tag == 'NN' and 'NNS' in self.tag_dictionary:
                keys = ['NNS']
            elif tag == 'NNPS' and 'NNP' in self.tag_dictionary:
                keys = ['NNP']
            elif tag == 'NNP' and 'NNPS' in self.tag_dictionary:
                keys = ['NNPS']
            else:
                assert False, tag

        if len(token) > 4:
            prefix = token[:-4]
        else:
            prefix = token[0]

        relevant_tag_prefix_tokens_with_tag = set()
        for k in keys:
            for token in self.vocab_with_prefix(prefix):
                assert isinstance(token, unicode), (repr(token), type(token))
                stemt = self.stemmer.stem(token)
                assert isinstance(stemt, unicode), (repr(stemt), type(stemt))
                stemtok = self.stemmer.stem(token)
                assert isinstance(stemtok, unicode), (repr(stemtok), type(stemtok))
                if stemt == stemtok:
                    if token in self.tag_dictionary[k]:
                        relevant_tag_prefix_tokens_with_tag.add((token, k))

        relevant_tag_prefix_tokens_with_tag.discard((token, tag))

        return sorted(relevant_tag_prefix_tokens_with_tag)

    def get_alternatives(self, token, tag):
        if self.cache.has_key( (token, tag) ):
            self.cache_stats[0] += 1 # hit
            alternatives = self.cache[(token, tag)]
            del(self.cache[(token, tag)])
            self.cache[(token, tag)] = alternatives
            return alternatives

        self.cache_stats[1] += 1 # miss

        if token == 'to':
            alternatives = self.closed_class_alternatives(token, 'IN') | self.closed_class_alternatives(token, 'AUX')
            alternatives.discard(('to', 'TO'))
        elif tag in closed_class_tags:
            alternatives = self.closed_class_alternatives(token, tag)
        elif token in AUX.keys():
            alternatives = self.closed_class_alternatives(token, 'AUX')
            alternatives.discard((token, tag))
        elif tag[:2] in ["NN", "VB"]:
            alternatives = self.open_class_alternatives(token, tag)
        else:
            alternatives = set([])

        self.cache[(token, tag)] = alternatives
        if len(self.cache) > self.cache_size:
            self.cache.popitem(last=False)

        assert (token, tag) not in alternatives, (token, tag)
        return alternatives

    def generate_path_variations(self, tagged_sentence, prob_of_err):

        prob_of_no_err = log10(1 - 10**prob_of_err)

        # TODO consider list of tuples instead of pair of parallel lists for the path_variations and path_error_terms

        # TODO consider changing the interface so only the last token and last tag get passed in

        # i'th element is a list of tokens
        path_variations = []

        # i'th element of path_error_terms is the probability of a
        # transformation leading to the observation (tagged_sentence)
        # from the i'th element of path variations.
        path_error_terms = []

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
                path_error_terms.append(prob_of_err - log10(len(token_variations)))

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
                path_error_terms.append(prob_of_err - log10(len(token_variations)))

                # Substitution and insertion
                for insertable in self.closed_class_insertables:
                    insertable_variations = self.get_alternatives(*insertable)
                    assert len(insertable_variations) != 0, repr(insertables) + ' : ' + repr(insertable_variations)

                    if len(tagged_sentence) == 1: # Substitution and insertion at beginning.
                        insertable = (insertable[0].title(), insertable[1])
                        if case == 't' or last_token == 'A':
                            path_variations.append(tagged_sentence[:-1] + [insertable] + [var])
                        else:
                            path_variations.append(tagged_sentence[:-1] + [insertable] + [recased_var])

                    else:
                        # Substitution and insertion not at beginning
                        path_variations.append(tagged_sentence[:-1] + [insertable] + [recased_var])
                    path_error_terms.append( 2*prob_of_err - log10(len(insertable_variations)) - log10(len(token_variations)) )

        for insertable in self.closed_class_insertables:
            insertable_variations = self.get_alternatives(*insertable)
            assert len(insertable_variations) != 0, repr(insertables) + ' : ' + repr(insertable_variations)

            possibly_recased_token = tagged_sentence[-1]

            # Insertion with no deletion or substitution
            if len(tagged_sentence) == 1:
                insertable = (insertable[0].title(), insertable[1])
                if case == 't':
                    possibly_recased_token = (last_token.lower(), last_tag)

            path_variations.append(tagged_sentence[:-1] + [insertable] + [possibly_recased_token])
            path_error_terms.append( prob_of_err - log10(len(insertable_variations)) + prob_of_no_err)

        assert len(path_variations) == len(path_error_terms), (len(path_variations), len(path_error_terms))
        return path_variations, path_error_terms

    def print_cache_stats(self):

        print "Cache hits:", self.cache_stats[0]
        print "Cache misses:", self.cache_stats[1]
