import argparse
import os
import csv

import numpy as np

from time import time
from itertools import takewhile, combinations
from operator import itemgetter

from parebrick.characters.unbalanced import write_characters_csv_unbalanced, call_unique_characters, write_trees_unbalanced

from parebrick.clustering.clustering import clustering, split_by_cluster

from parebrick.utils.data.converters import block_coords_to_infercars
from parebrick.utils.data.parsers import genome_lengths_from_block_coords, parse_infercars_to_df, \
    get_genomes_contain_blocks_grimm, make_labels_dict
from parebrick.utils.data.unique_gene_filters import grimm_filter_unique_gene, filter_dataframe_unique
from parebrick.utils.data.stats import distance_between_blocks_dict, check_stats_stains, get_mean_coverage

from parebrick.utils.decorators import decorate

from parebrick.tree.tree_holder import TreeHolder

# argument parsing
parser = argparse.ArgumentParser(
    description='Based on synteny blocks and phylogenetic tree this tool calls parallel rearrangements.')

parser.add_argument('--tree', '-t', required=True, help='Tree in newick format, must be parsable by ete3 library.'
                                                        'You can read more about formats supported by ete3 at http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#reading-and-writing-newick-trees')
parser.add_argument('--blocks_folder', '-b', required=True,
                    help='Path to folder with blocks resulted as output of original Sibelia or maf2synteny tool.')
parser.add_argument('--labels', '-l', default='', help='Path to csv file with tree labels, must contain two columns: `strain` and `label`.')
parser.add_argument('--output', '-o', required=True, help='Path to output folder.')

show_branch_support = True
clustering_proximity_percentile = 25
clustering_threshold = 0.1
clustering_j = 0.75
clustering_b = 0.25

GRIMM_FILENAME = 'genomes_permutations.txt'
UNIQUE_GRIMM_FILENAME = 'genomes_permutations_unique.txt'

BLOCKS_COORD_FILENAME = 'blocks_coords.txt'
INFERCARS_FILENAME = 'blocks_coords.infercars'

STATS_FILE = 'stats.csv'
BALANCED_FOLDER = 'balanced_rearrangements_output/'
UNBALANCED_FOLDER = 'un' + BALANCED_FOLDER

CHARACTERS_FOLDER = 'characters/'
TREES_FOLDER = 'tree_colorings/'

BALANCED_COLORS = ['White', 'Gainsboro', 'LightGreen', 'LightBlue', 'NavajoWhite', 'LightPink', 'LightCoral', 'Purple',
                   'Navy', 'Olive', 'Teal', 'SaddleBrown', 'SeaGreen', 'DarkCyan', 'DarkOliveGreen', 'DarkSeaGreen']

UNBALANCED_COLORS = ['Gainsboro', 'White'] + BALANCED_COLORS[2:]

# This module converts data from the output data format
# of Sibelia or Ragout scripts into the infercars format to simplify the subsequent annotation.
# Also filtering blocks in the grimm format for unique single-copy blocks for the breakpoint graph construction.
@decorate("Preprocess Data")
def preprocess_data():
    global unique_blocks
    unique_blocks = grimm_filter_unique_gene(blocks_folder + GRIMM_FILENAME, preprocessed_data_folder + UNIQUE_GRIMM_FILENAME)
    print('Converting block coords to infercars format')
    block_coords_to_infercars(blocks_folder + BLOCKS_COORD_FILENAME, preprocessed_data_folder + INFERCARS_FILENAME)

# In this module, parsing of input blocks and their coordinates, as well as a phylogenetic, takes place.
# Next, some statistics are calculated: the total number of blocks,
# the number of unique single-copy blocks, as well as the percentage of genome coverage with these two types of blocks.
# After that, the correspondence of strains set on the phylogenetic tree and strains set in the synthenic blocks
# is checked, if necessary, the missing strains are discarded.
@decorate("Parsers and check strains")
def parsers_and_stats():
    global genome_lengths, blocks_df, tree_holder, genomes, blocks, block_genome_count

    genome_lengths = genome_lengths_from_block_coords(blocks_folder + BLOCKS_COORD_FILENAME)
    blocks_df = parse_infercars_to_df(preprocessed_data_folder + INFERCARS_FILENAME)
    unique_blocks_df = filter_dataframe_unique(blocks_df)

    print('Blocks count:', len(blocks_df['block'].unique()))
    print('Unique one-copy blocks count:', len(unique_blocks_df['block'].unique()))

    print('Mean block coverage:', get_mean_coverage(blocks_df, genome_lengths) * 100, '%')
    print('Mean unique one-copy blocks coverage:', get_mean_coverage(unique_blocks_df, genome_lengths) * 100, '%')
    print()

    tree_holder = TreeHolder(tree_file, labels_dict=make_labels_dict(labels_file))

    genomes, blocks, block_genome_count = get_genomes_contain_blocks_grimm(blocks_folder + GRIMM_FILENAME)

    genomes = check_stats_stains(tree_holder, set(genomes))

# In this module, the mapping of blocks by its number for each strain is performed.
@decorate("Unbalanced rearrangements characters")
def unbalanced_rearrangements_characters():
    global ub_characters, blocks
    print('All:', len(blocks))
    blocks = [block for block in blocks if any(copies == 2 for copies in block_genome_count[block].values())]
    print('Only duplicated:', len(blocks))

    ub_characters = [{genome: block_genome_count[block][genome] for genome in genomes}
                     for block in blocks]

def count_parallel_rearrangements(tree_holder, skip_grey):
    score, count, count_all  = 0, 0, 0
    leaves_count = []
    for color, nodes in tree_holder.innovations.items():
        if color == 2:
            for node in nodes:
                leaves_count.append(len(node))

        if len(nodes) <= 1 or (skip_grey and color == 1): continue
        count += 1
        count_all += len(nodes)
        for n1, n2 in combinations(nodes, 2):
            score += n1.get_distance(n2)

    min_leaves, median_leaves, max_leaves = np.min(leaves_count), np.median(leaves_count), np.max(leaves_count)
    return score, count, count_all, min_leaves, median_leaves, max_leaves

def get_characters_stats_unbalanced(blocks, characters, tree_holder):
    ans = []
    for block, genome_colors in zip(blocks, characters):
        tree_holder.count_innovations_fitch(genome_colors)

        have = sum(map(lambda c: c > 0, genome_colors.values()))
        all_leaves = sum(map(lambda c: c == 2, genome_colors.values()))

        stats = count_parallel_rearrangements(tree_holder, skip_grey=False)
        ans.append([block, *stats, have, all_leaves])

    return ans

@decorate("Unbalanced rearrangements stats and clustering")
def unbalanced_rearrangements_stats_and_clustering():
    global ub_cls, ub_characters, ub_stats

    ub_stats = get_characters_stats_unbalanced(blocks, ub_characters, tree_holder)

    char_stats = zip(ub_characters, ub_stats)
    print('Got characters after copy number variation consideration:', len(blocks))
    # sorting for get most interesting characters in the beginning
    char_stats = sorted(char_stats, key=lambda r: (r[1][8], r[1][6]), reverse=True)
    # remove convex characters
    # char_stats = list(takewhile(lambda r: r[1][3] > 1, char_stats))

    # print('Left non-convex characters after filtering:', len(char_stats))

    # unzip
    ub_characters = [char for char, stat in char_stats]
    ub_stats = [stat for char, stat in char_stats]

    print('Counting distances between non-convex character blocks, may take a while')
    distance_between_blocks = distance_between_blocks_dict(blocks_df, genome_lengths, set(map(itemgetter(0), ub_stats)))
    ub_cls = clustering(ub_characters, ub_stats, distance_between_blocks, max(genome_lengths.values()),
                        clustering_threshold, clustering_j, clustering_b, clustering_proximity_percentile)

    print('Clusters:', np.unique(ub_cls).shape[0])

def write_stats_csv_unbalanced(stats, cls, stats_file):
    rows = [['block', 'cluster', 'parallel_rear_score', 'parallel_rear_unique_innovation_count',
             'parallel_rear_all_innovations_count', 'min_dup_leaves', 'median_dup_leaves', 'max_dup_leaves',
             'leaves_have_block', 'leaves_have_duplication']] + \
           [stat[0:1] + [cl] + stat[1:] for stat, cl in zip(stats, cls)]
    with open(stats_file, 'w') as f:
        wtr = csv.writer(f)
        wtr.writerows(rows)

@decorate('Unbalanced rearrangements output')
def unbalanced_rearrangements_output():
    unbalanced_folder = output_folder + UNBALANCED_FOLDER
    os.makedirs(unbalanced_folder, exist_ok=True)

    stats_file = unbalanced_folder + STATS_FILE
    write_stats_csv_unbalanced(ub_stats, ub_cls, stats_file)

    characters_folder = unbalanced_folder + CHARACTERS_FOLDER

    cls_chars, cls_stats = split_by_cluster(ub_characters, ub_stats, ub_cls)
    unique_chars_list = call_unique_characters(cls_chars, cls_stats)

    write_characters_csv_unbalanced(unique_chars_list, characters_folder)

    trees_folder = unbalanced_folder + TREES_FOLDER
    write_trees_unbalanced(unique_chars_list, trees_folder, show_branch_support, tree_holder, UNBALANCED_COLORS)


if __name__ == "__main__":
    start_time = time()
    d = vars(parser.parse_args())
    blocks_folder, output_folder, tree_file, labels_file = d['blocks_folder'], d['output'], d['tree'], d['labels']

    # folders
    if blocks_folder[:-1] != '/': blocks_folder += '/'
    if output_folder[:-1] != '/': output_folder += '/'

    preprocessed_data_folder = output_folder + 'preprocessed_data/'
    os.makedirs(preprocessed_data_folder, exist_ok=True)

    preprocess_data()
    parsers_and_stats()

    unbalanced_rearrangements_characters()
    unbalanced_rearrangements_stats_and_clustering()
    unbalanced_rearrangements_output()

    print('Total elapsed time:', time() - start_time)