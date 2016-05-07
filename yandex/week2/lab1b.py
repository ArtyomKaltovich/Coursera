import os, sys
import pandas
import sklearn.datasets
from sklearn.preprocessing import scale
from sklearn.neighbors import KNeighborsRegressor
from sklearn.cross_validation import KFold, cross_val_score
from numpy import linspace, mean
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def cross_validate(df):
	accuracies = []
	params = []
	kf = KFold(len(df.target), n_folds=5, shuffle=True, random_state=42)
	for p in linspace(1., 10., 100):
		regressor = KNeighborsRegressor(n_neighbors=5, weights='distance', metric='minkowski', p = p)
		score = cross_val_score(regressor, X=df.data, y=df.target, cv=kf, scoring='mean_squared_error')
		accuracies.append(mean(score))
		params.append(p)
	return accuracies, params


def calculate_max_accuracies(df):
	accuracies, params = cross_validate(df)
	max_accuracy = max(accuracies)
	index = accuracies.index(max_accuracy)
	return(params[index])


df = sklearn.datasets.load_boston()
df.data = scale(df.data)
index = calculate_max_accuracies(df)
io_yandex.print_result(io_yandex.one_digit_round(index), "1b.txt")