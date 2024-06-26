#!usr/bin/env python
# -*- coding: UTF-8 -*-

"""
加载数据，滑动平均，PCA降维
"""

import os
import json

import pandas as pd
from sklearn.utils import Bunch
from sklearn.decomposition import PCA
from numpy import ones, zeros, concatenate, array, convolve

from model import save_model


def get_train_data(train_set_path: str) -> Bunch:
    plastic = pd.DataFrame()
    notplastic = pd.DataFrame()

    for root, subdirs, files in os.walk(os.path.join(train_set_path, "塑料")):
        for file in files:
            temp = pd.read_csv(os.path.join(root, file),
                               header=None, usecols=[0, 1], index_col=0)
            plastic = pd.concat([plastic, temp], axis=1)

    for root, subdirs, files in os.walk(os.path.join(train_set_path, "非塑料")):
        for file in files:
            temp = pd.read_csv(os.path.join(root, file),
                               header=None, usecols=[0, 1], index_col=0)
            notplastic = pd.concat([notplastic, temp], axis=1)

    spectrum = Bunch()
    spectrum["data"] = pd.concat((plastic, notplastic), axis=1).values.T
    spectrum["target"] = concatenate((ones(plastic.shape[1]),
                                      zeros(notplastic.shape[1])))
    spectrum["feature_names"] = plastic.index.values
    spectrum["target_names"] = array(['plastic', 'notplastic'], dtype='<U10')

    return spectrum


def getData(file_path: str) -> Bunch:
    with open(file_path) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    spectrum = Bunch()
    spectrum["data"] = df.values
    spectrum["feature_names"] = df.columns.values

    return spectrum


def slideAvg(spectrum: Bunch, width: int = 5) -> None:
    kernel = ones(width)/width
    avg = list()
    for data in spectrum["data"]:
        avg.append(convolve(data, kernel, "same"))
    avg = array(avg)
    spectrum["data"] = avg
    return None


def PCADR(spectrum: Bunch, labeled: bool, save: bool) -> PCA:
    data = pd.DataFrame(spectrum["data"], columns=spectrum["feature_names"])
    pca = PCA(15)
    newdata = pca.fit_transform(data.iloc[:, 0:-1])

    if labeled:
        output = pd.DataFrame(newdata, index=data.index)
        data["output"] = spectrum['target']
        output['output'] = data['output']

    if save:
        output.to_csv('pcaed.csv')

    return pca


if __name__ == '__main__':
    spectrum = get_train_data("data_csv")
    slideAvg(spectrum)
    save_model(PCA=PCADR(spectrum, labeled=True, save=True))
