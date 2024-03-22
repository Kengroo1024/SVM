#!usr/bin/env python
# -*- coding: UTF-8 -*-

from pandas import read_csv, DataFrame
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from numpy import logical_xor
import pickle


def SVM_model(train: DataFrame) -> svm.SVC:
    feature = train.iloc[:, 0:-1].values
    target = train["output"].values
    clf = svm.SVC()
    return clf.fit(feature, target)


def MLP_model(train: DataFrame) -> MLPClassifier:
    feature = train.iloc[:, 0:-1].values
    target = train["output"].values
    clf = MLPClassifier()
    return clf.fit(feature, target)


def save_model(**kwargs) -> None:
    for key, value in kwargs.items():
        with open(key+".pickle", "wb") as f:
            f.write(pickle.dumps(value))
    return None


def load_model(path: str):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data


if __name__ == '__main__':
    data = read_csv("pcaed.csv", index_col=0)
    train, test = train_test_split(data, random_state=89756)

    clf = SVM_model(train)

    # clf = MLP_model(train)

    save_model(SVM=clf)

    # clf = load_model("bestModel/MLP.pickle")

    a = clf.predict(test.iloc[:, 0:-1])
    # print(logical_xor(a, test["output"].values))
    print((1-logical_xor(a, test["output"].values).sum()/a.shape[0])*100)
