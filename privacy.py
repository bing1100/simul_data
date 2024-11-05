import numpy as np
import math
import pandas as pd
from collections import Counter

def combinations(df, qi):
    col = qi + ['key', 'count']
    ldf = df[qi].values.tolist()
    ldf = ["_".join([str((v)) for v in r]) for r in ldf]
    cldf = Counter(ldf)
    ldf = [k.split("_") + [k, v] for k, v in list(cldf.items())]
    fdf = pd.DataFrame(ldf, columns=col).sort_values(by=['count'], ascending=False)
    return fdf

def add(df, qi_sv, qi, intersection):
    c = df.copy()
    ldf = df[qi_sv].values.tolist()
    ldf = ["_".join([str(v) for v in r]) in intersection for r in ldf]
    c['ls_rs'] = np.where(ldf, 1, 0)

    ldf = df[qi].values.tolist()
    ldf = ["_".join([str(v) for v in r]) for r in ldf]
    cldf = Counter(ldf)
    c['QI'] = ldf
    c['QI_count'] = [cldf[r] for r in c['QI']]
    return c

def syntheticCombinations(df, cdf):
    col = list(df.columns) + ['key','syn_count']
    ldf = df.values.tolist()
    ldf = ["_".join([str(v) for v in r]) for r in ldf]
    cldf = Counter(ldf)
    ldf = [k.split("_") + [k, v] for k, v in list(cldf.items())]
    fdf = pd.DataFrame(ldf, columns=col).sort_values(by=['syn_count'], ascending=False)
    display(fdf)
    display(cdf)
    return cdf.merge(fdf, how='left', on='key')

def removeSyntheticOutliers(df, threshold):
    col = list(df.columns) 
    col.remove('count')
    col.remove('syn_count')
    col.remove('key')
    l = []
    for index, row in df.iterrows():
        c = row['count']
        sc = row['syn_count']
        if c >= threshold and not math.isnan(sc):
            l.extend([[row[n] for n in col]]*int(sc))
    fdf = pd.DataFrame(l, columns=col).sample(frac=1).reset_index(drop=True)
    return fdf