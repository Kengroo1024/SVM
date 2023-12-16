#!usr/bin/env python
# -*- coding: UTF-8 -*-

"""
加载数据，滑动平均，PCA降维
"""

import pandas as pd
import os
from sklearn.utils import Bunch
from sklearn.decomposition import PCA
from numpy import ones, zeros, concatenate, array, convolve


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


def slideAvg(spectrum: Bunch, width: int = 5) -> None:
    kernel = ones((width,))/width
    avg = list()
    for data in spectrum["data"]:
        avg.append(convolve(data, kernel, "same"))
    avg = array(avg)
    spectrum["data"] = avg
    return None


def PCADR(spectrum: Bunch) -> None:
    data = pd.DataFrame(spectrum["data"], columns=spectrum["feature_names"])
    data["output"] = spectrum['target']

    pca = PCA(15)
    output = pd.DataFrame(pca.fit_transform(
        data.iloc[:, 0:-1]), index=data.index)
    output['output'] = data['output']
    output.to_csv('pcaed.csv')

    return None


if __name__ == '__main__':
    spectrum = get_data()
    slideAvg(spectrum)
    PCADR(spectrum)
