#!usr/bin/env python
# -*-coding: UTF-8 -*-

"""
加载数据并且使用PCA降维
"""

from pdb import run
import pandas as pd
import os
from sklearn.utils import Bunch
from sklearn.decomposition import PCA
from numpy import ones, zeros, concatenate, array
from sklearn.model_selection import train_test_split


def get_data():
    plastic = pd.DataFrame()
    notplastic = pd.DataFrame()

    for path, folders, files in os.walk(os.path.join("data_csv", "塑料")):
        for file in files:
            temp = pd.read_csv(os.path.join(path, file),
                               header=None, usecols=[0, 1], index_col=0)
            plastic = pd.concat([plastic, temp], axis=1)

    for path, folders, files in os.walk(os.path.join("data_csv", "非塑料")):
        for file in files:
            temp = pd.read_csv(os.path.join(path, file),
                               header=None, usecols=[0, 1], index_col=0)
            notplastic = pd.concat([notplastic, temp], axis=1)

    spectrum = Bunch()
    spectrum["data"] = pd.concat((plastic, notplastic), axis=1).values.T
    spectrum["target"] = concatenate((ones(plastic.shape[1]),
                                      zeros(notplastic.shape[1])))
    spectrum["feature_names"] = plastic.index.values
    spectrum["target_names"] = array(['plastic', 'notplastic'], dtype='<U10')

    return spectrum


if __name__ == '__main__':
    spectrum = get_data()
    data = pd.DataFrame(spectrum["data"], columns=spectrum["feature_names"])
    data["output"] = spectrum['target']

    pca = PCA(15)
    output = pd.DataFrame(pca.fit_transform(
        data.iloc[:, 0:-1]), index=data.index)
    output['output'] = data['output']

    output.to_csv('pcaed.csv')
