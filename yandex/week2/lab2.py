import os, sys
import pandas
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex

def load_data():
	data_train = pandas.read_csv('../data/perceptron-train.csv', header=None)
	classes_train, data_train = io_yandex.get_value_column(data_train, 0)
	data_test = pandas.read_csv('../data/perceptron-test.csv', header=None)
	classes_test, data_test = io_yandex.get_value_column(data_test, 0)
	return data_train, classes_train, data_test, classes_test


def scale_data(*arg):
	scaler = StandardScaler()
	X_train_scaled = scaler.fit_transform(arg[0])
	yield X_train_scaled
	for a in arg[1:]:
		yield scaler.transform(a)

def teach(data_train, classes_train, data_test):
	clf = Perceptron(random_state=241)
	clf.fit(data_train, classes_train)
	classes_predictions = clf.predict(data_test)
	return classes_predictions


data_train, classes_train, data_test, classes_test = load_data()
predictions = teach(data_train, classes_train, data_test)
non_scaled_accuracies = accuracy_score(classes_test, predictions)
print(non_scaled_accuracies)

data_train, data_test = scale_data(data_train, data_test)
predictions = teach(data_train, classes_train, data_test)
scaled_accuracies = accuracy_score(classes_test, predictions)
print(scaled_accuracies)

io_yandex.print_result(io_yandex.three_digit_round((scaled_accuracies - non_scaled_accuracies)), "2_2.txt") 