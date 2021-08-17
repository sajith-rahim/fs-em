import os
import pandas as pd

from algorithm.fsem import FellegiSunterEM
from preprocessing.process import PreProcessRLData


def run():
    # load data
    df_src = pd.read_csv("./data/RL1.csv")
    df_target = pd.read_csv("./data/RL2.csv")

    print(df_target.head(3))
    print(df_src.head(3))

    # pre-process
    pre = PreProcessRLData(source_dataframe=df_src, target_dataframe=df_target, key_column='id')
    pairs = pre.generate_pairs(method='jaro', threshold=0.5)

    print(pairs)
    # print(pairs.fname.value_counts())

    agreement_matrix = pairs.drop(labels=['M_ID', 'S_ID'], axis=1).to_numpy()
    print(agreement_matrix)

    # EM
    fs_em = FellegiSunterEM(df_src, df_target)
    res = fs_em.run_em(agreement_matrix, tolerance=0.001, max_iter=10000)

    # print results
    for attr, v in res.items():
        print(attr, '=>', v)
