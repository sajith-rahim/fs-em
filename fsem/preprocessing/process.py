import pandas as pd
import itertools

from fsem.similarity_measures.jaro import get_jaro_distance
from fsem.similarity_measures.levenshtein import levenshtein_similarity


class PreProcessRLData:

    def __init__(self, source_dataframe, target_dataframe, key_column, attr_function_map={}):
        self.source_dataframe = source_dataframe
        self.target_dataframe = target_dataframe
        self.attr_fn_map = attr_function_map
        self.key_column = key_column

    def generate_pairs(self, method='jaro', threshold=0.7):
        nB, k = self.target_dataframe.shape

        sim_mat = []

        for idx in range(nB):
            sim_mat.append(
                list(
                    self.source_dataframe.apply(
                        self.sim_compare, axis=1, rowB=self.target_dataframe.iloc[idx],
                        key_col='id', attr_function_map=self.attr_fn_map)
                )
            )

        attrs = ['M_ID', 'S_ID'] + [attr for attr in list(self.target_dataframe.columns) if attr != self.key_column]
        return pd.DataFrame(list(itertools.chain(*sim_mat)), columns=attrs)

    def sim_compare(self, rowA, rowB, key_col, attr_function_map={}, method='jaro', threshold=0.7):
        agg_row = [getattr(rowA, key_col), getattr(rowB, key_col)]
        for attr, val in rowA.iteritems():
            if attr != key_col:
                if isinstance(val, str):
                    if method == 'jaro':
                        _sim = 1.0 if get_jaro_distance(val, getattr(rowB, attr)) else 0.0
                    elif method == 'levenshtein':
                        _sim = 1.0 if levenshtein_similarity(val, getattr(rowB, attr)) > threshold else 0.0
                    else:
                        _sim = 0.0
                elif val == getattr(rowB, attr):
                    _sim = 1.0
                else:
                    _sim = 0.0
                agg_row.append(_sim)

        return agg_row
