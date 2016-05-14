import os, sys
import pandas
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import log_loss
import numpy
import matplotlib.pyplot as plt
PACKAGE_PARENT = "../.."
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def load_data(path):
    train = pandas.read_csv(path)
    #train = train.head(100)
    target, train = io_yandex.get_value_column(train, 'Activity')
    train = train.values
    X_train, X_test, y_train, y_test = \
    		train_test_split(train, target, test_size=0.8, random_state=241)
    return X_train, X_test, y_train, y_test


def fit_and_log_loss(X_train, y_train, learning_rate):
	#clf = GradientBoostingClassifier(n_estimators=250, verbose=True, random_state=241)
	clf = GradientBoostingClassifier(learning_rate=learning_rate,
		n_estimators=250, verbose=False, random_state=241)
	clf.fit(X_train, y_train)
	train_score = clf.staged_predict_proba(X_train)
	test_score = clf.staged_predict_proba(X_test)
	train_loss = [ log_loss(y_train, pred) for pred in train_score]
	test_loss = [ log_loss(y_test, pred) for pred in test_score]
	return train_loss, test_loss


def draw_plot(learning_rate, train_loss, test_loss, index):
	plt.figure()
	plt.title('Learning rate = ' + str(learning_rate))
	plt.plot(test_loss, 'r', linewidth=2)
	plt.plot(train_loss, 'g', linewidth=2)
	plt.legend(['test', 'train'])
	plt.savefig(str(index) + '.png')


X_train, X_test, y_train, y_test = load_data('gbm-data.csv')
min_res = 1
for index, learning_rate in enumerate([1, 0.5, 0.3, 0.2, 0.1], start=1):
	train_loss, test_loss = fit_and_log_loss(X_train, y_train, learning_rate)
	draw_plot(learning_rate, train_loss, test_loss, index)
	if index == 4: # learning_rate = 0.2
		min_res = numpy.argmin(test_loss)
		io_yandex.print_result(io_yandex.two_digit_round(test_loss[min_res])
			+ ' ' + str(min_res), '2.txt')

io_yandex.print_result('overfitting', '1.txt')

min_res = 37
clf = RandomForestClassifier(n_estimators=min_res, random_state=241)
clf.fit(X_train, y_train)
train_score = clf.predict_proba(X_train)
test_score = clf.predict_proba(X_test)
test_loss = log_loss(y_test, test_score)
io_yandex.print_result(io_yandex.two_digit_round(test_loss), '3.txt')
	