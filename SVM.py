#!usr/bin/env python
# -*-coding: UTF-8 -*-

from pandas import read_csv, DataFrame
from sklearn import svm
from sklearn.model_selection import train_test_split
from numpy import logical_xor, logical_not


def get_model(train: DataFrame):
    feature = train.iloc[:, 0:-1].values
    target = train["output"].values
    clf = svm.SVC()
    return clf.fit(feature, target)


data = read_csv("pcaed.csv", index_col=0)
train, test = train_test_split(data, random_state=1092)

clf = get_model(train)

a = clf.predict(test.iloc[:, 0:-1])
print(logical_xor(a, test["output"].values))
print((1-logical_xor(a, test["output"].values).sum()/a.shape[0])*100)
