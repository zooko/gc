# L. Amber Wilcox-O'Hearn 2013
# ScoreIntegrator.py

# For every file matching data_directory + 'seed_' + int/scores_trigram_model_size_XK_[pos or closed_class]_weight_Yerror_prob_Z:
# read the 9th, 8th and 7th last lines to get the edits, gold, correct.
# Calculate p, r, f
# Write to data_dir

# scores_trigram_model_size_10K_pos_weight_0.7error_prob_-1.3

import os
from collections import defaultdict

def precision_recall_fmeasure(correct, proposed, gold):
    p = 1.0*correct/proposed
    r = 1.0*correct/gold
    if p+r == 0: f = 0
    else: f = 2.0*(p*r)/(p+r)
    return (p, r, f)

def integrate_scores(data_directory):

    pos_params = defaultdict(list)
    closed_class_params = defaultdict(list)

    seeds = [d for d in os.listdir(data_directory) if d.startswith('seed_')]
    for seed in seeds:
        score_files = [s for s in os.listdir(data_directory + seed) if s.startswith('scores_')]
        for score_file_name in score_files:
            vocabulary_size, rest = score_file_name.split('scores_trigram_model_size_')[1].rsplit('K_')
            try:
                pos_weight, error_probability = rest.split('pos_weight_')[1].rsplit('error_prob_')
                pos_params[(vocabulary_size, pos_weight, error_probability)].append(data_directory+'/'+seed+'/'+score_file_name)
            except (ValueError, IndexError):
                closed_class_weight, error_probability = rest.split('closed_class_weight_')[1].rsplit('error_prob_')
                closed_class_params[(vocabulary_size, pos_weight, error_probability)].append(data_directory+'/'+seed+'/'+score_file_name)

    results = defaultdict()

    for k in pos_params.keys():
        
        correct = []
        proposed = []
        gold = []
        for score_file_name in pos_params[k]:
            lines = open(score_file_name, 'r').readlines()
            tokens = lines[-9].split()
            assert tokens[0] == 'CORRECT', tokens
            correct.append(float(tokens[-1]))
            tokens = lines[-8].split()
            assert tokens[0] == 'PROPOSED', tokens
            proposed.append(float(tokens[-1]))
            tokens = lines[-7].split()
            assert tokens[0] == 'GOLD', tokens
            gold.append(float(tokens[-1]))


        precision, recall, fmeasure = precision_recall_fmeasure(sum(correct), sum(proposed), sum(gold))
        results[k] = (precision, recall, fmeasure)

    return results



    



