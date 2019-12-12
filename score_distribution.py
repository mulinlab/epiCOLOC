import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_merged = pd.DataFrame([])
DS = '/g/zhouyao/datasets/epiCOLOC/results/'
with open('sampling/sampling.txt') as fp:
    for line in fp:
        df = pd.read_csv(DS + line.strip() + '/results.csv')
        df_merged = df_merged.append(df)
df_all = df_merged[df_merged['log_p_value']>-np.log10(0.05)]
f = plt.figure()
n, bins, patches = plt.hist(df_all.combo_score.values, color= '#0504aa',
                            bins=1600, alpha=0.7, rwidth=0.85, density=True)

plt.xlim(-10, 10)
plt.xlabel('Combo Score',fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.ylabel('Probability',fontsize=12)
plt.title('Combo Score Distribution',fontsize=15)

f.savefig('supp2.svg', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches='tight', pad_inches=0.8,
        frameon=None, metadata=None, figsize=[6.4, 4.8])        
