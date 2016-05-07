import os, sys
import pandas
import numpy
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_curve
PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def calculate_prediction_type(true, pred):
	tp = 0; fp = 0; fn = 0; tn = 0
	for i, j in zip(true, pred):
		if (i == 0 and j == 0 ):
			tn += 1
		elif (i == 0 and j == 1 ):
			fp += 1
		elif (i == 1 and j == 0 ):
			fn += 1
		elif (i == 1 and j == 1 ):
			tp += 1
	return tp, fp, fn, tn


def calculate_scores(true, pred):
	accuracy = accuracy_score(true, pred)
	precision = precision_score(true, pred)
	recall = recall_score(true, pred)
	f1 = f1_score(true, pred)
	return accuracy, precision, recall, f1


def calculate_roc_auc(true, *arg):
	for a in arg:
		score = roc_auc_score(true, a)
		yield score


def largest_index(a):
    return numpy.argsort(a)[::-1][:1]


data = pandas.read_csv("./data/classification.csv")
tp, fp, fn, tn = calculate_prediction_type(data["true"], data["pred"])
io_yandex.print_result(" ".join(map(io_yandex.two_digit_round,
	[tp, fp, fn, tn])), "4_1.txt")
accuracy, precision, recall, f1 = calculate_scores(data["true"], data["pred"])
io_yandex.print_result(" ".join(map(io_yandex.two_digit_round,
	[accuracy, precision, recall, f1])), "4_2.txt")


data = pandas.read_csv("./data/scores.csv")
print(list(data.columns.values))
logreg, svm, knn, tree = calculate_roc_auc(data["true"], data["score_logreg"],
	data["score_svm"], data["score_knn"], data["score_tree"])
index = largest_index([logreg, svm, knn, tree]) + 1 # first is "true"
io_yandex.print_result("".join(data.columns.values[index]), "4_3.txt") #"".join is used to remove [' and '] symbols

max_val = 0
max_name = data.columns.values[2]
for index in range(2, len(data.columns.values)):
	precision, recall, thresholds = precision_recall_curve(data["true"], data[data.columns.values[index]])
	for i, j in zip(precision, recall):
		if j > 0.7 and max_val < i:
			max_val = i
			max_name = data.columns.values[index]
io_yandex.print_result(max_name, "4_4.txt")