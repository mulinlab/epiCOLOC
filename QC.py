import subprocess
from concurrent import futures

import os
import pandas as pd
import io
import numpy as np
from collections import defaultdict
from scipy.cluster.hierarchy import dendrogram, linkage  
from scipy.cluster.hierarchy import inconsistent, fcluster,ward
from scipy.spatial.distance import pdist

import argparse

parser = argparse.ArgumentParser(description='outlier removing with inconsistent methods')
parser.add_argument('--input', help='profiles folder path')
parser.add_argument('--output', help='metrics path')
args = parser.parse_args()

DS_path = args.input
DS_list = sorted(os.listdir(DS_path))

def inconsistent_filter(results, files):
    matrix = pd.DataFrame([], index=files)
    results = results.replace('.bed.gz','')
    results_table = pd.read_csv(io.StringIO(results), sep='\t', header=None)
    results_table.columns = ['query', 'filename', 'size', 'overlaps', 'odds_ratio', 'fishers_two_tail', 'fishers_left_tail', 'fishers_rigth_tail', 'combo_score']
    files = [x.replace('.bed.gz','') for x in files]
    n_files = ith_file
    for name, group in results_table.groupby(by=['query']):
        matrix[name] = group.combo_score.values 

    Z = ward(pdist(matrix))
    depth = 5
    matrix['clusters'] = fcluster(Z, depth=depth, t=2, criterion='inconsistent')
    
    return matrix

def filter_cluser(DS):
    DS = DS_path + DS
    index_path = DS + '/giggle_index'
    results = ''
    ith_file = 0
    files = []
    for file in sorted(os.listdir(DS)):
        if not file.endswith('.gz') : 
            continue
        ith_file += 1
        files += [file]
        file_path = os.path.join(DS, file)
        cmdline = f'giggle search -i {index_path} -q {file_path} -s'
        result = subprocess.check_output(cmdline, shell=True).decode('utf-8').replace('\t\n', '\n')
        results = results + file + '\t' + (f'\n{file}\t').join(result.split("\n")[1:-1]) + "\n"
    matrix = pd.DataFrame([], index=files)
    if ith_file >= 3:
        matrix = inconsistent_filter(results, files)
    return matrix, DS.replace(DS_path, '')
        
with futures.ProcessPoolExecutor(max_workers=4) as executor:
    for future in executor.map(filter_cluser):
        future.to_csv(args.output,index=False)
