#!usr/bin/env python
# -*-coding: UTF-8 -*-

"""
加载数据并且使用PCA降维
"""

import pandas as pd
import os
from sklearn.decomposition import PCA

plastic = list()
notplastic = list()


for path, folders, files in os.walk(os.path.join("data_csv", "塑料")):
    for file in files:
        plastic.append(pd.read_csv(os.path.join(path, file),
                       header=None, usecols=[0, 1]).values)
for path, folders, files in os.walk(os.path.join("data_csv", "非塑料")):
    for file in files:
        notplastic.append(pd.read_csv(os.path.join(
            path, file), header=None, usecols=[0, 1]).values)
