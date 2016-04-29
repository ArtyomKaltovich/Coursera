import os, sys
import pandas
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import KFold
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import scale
from numpy import mean
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def cross_validate(df, classes, kf):
	accuracies = []
	for i in range(1,51):
		classifier = KNeighborsClassifier(n_neighbors=i)
		score = cross_val_score(classifier, X=df, y=classes, cv=kf)
		accuracies.append(mean(score))
	return accuracies


def calculate_max_accuracies(df, classes, kf):
	accuracies = cross_validate(df, classes, kf)
	max_accuracy = max(accuracies)
	n_neighbors = accuracies.index(max_accuracy) + 1  # first index is 0. It is for 1 class
	print(accuracies[2])
	return n_neighbors, max_accuracy


def print_n_neighbors_and_accuracies(df, classes, kf, path1, path2):
	n_neighbors, max_accuracy = calculate_max_accuracies(df, classes, kf)
	max_accuracy = io_yandex.two_digit_round(max_accuracy)
	io_yandex.print_result(str(n_neighbors), path1)
	io_yandex.print_result(max_accuracy, path2)


df = io_yandex.load_wine_to_dataframe()
classes, df = io_yandex.get_value_column(df, 0)
kf = KFold(len(df.index), n_folds=5, shuffle=True, random_state=42)
print_n_neighbors_and_accuracies(df, classes, kf, "1.txt", "2.txt")
df = scale(df)
print_n_neighbors_and_accuracies(df, classes, kf, "3.txt", "4.txt")