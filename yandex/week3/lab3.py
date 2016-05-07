# Thanks https://github.com/dstarcev/coursera-machine-learning-yandex/blob/master/week3/assignment3/main.py
import os,sys
import pandas
import numpy
from sklearn.metrics import roc_auc_score
from scipy.spatial import distance
from sklearn.linear_model import LogisticRegression
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def split(data):
    X = data.iloc[:,1:].values
    y = data.iloc[:,0].values
    return X, y


def sigmoid(X, w):
    return 1 / (1 + numpy.exp(-numpy.dot(X, w)))


def cost(X, y, w, C):
    sum = 0
    n = X.shape[0]
    m = X.shape[1]
    for i in range(n):
        sum += numpy.log(1 + numpy.exp(-y[i] * numpy.dot(X[i], w)))
    reg = C * (w ** 2).sum() / m
    cost = sum / numpy.double(n) + reg
    return cost


def train(X, y, k, C):
    n = X.shape[0]
    m = X.shape[1]
    w = numpy.zeros(m)
    c = cost(X, y, w, C)
    threshold = 1e-5
    for iteration in range(10000):
        new_w = numpy.zeros(m)
        for j in range(m):
            sum = 0
            for i in range(n):
                sum += y[i] * X[i, j] * (1 - 1 / (1 + numpy.exp(-y[i] * numpy.dot(X[i], w))))
            new_w[j] = w[j] + k * sum / numpy.double(n) - k * C * w[j]
        new_cost = cost(X, y, new_w, C)
        if distance.euclidean(w, new_w) <= threshold:
            return new_w
        c = new_cost
        w = new_w
    return w


data = pandas.read_csv('./data/data-logistic.csv', header=None)
X, y = split(data)
k = 0.1
score = roc_auc_score(y, sigmoid(X, train(X, y, k, C = 0)))
score_reg = roc_auc_score(y, sigmoid(X, train(X, y, k, C = 10)))
print(score, score_reg)