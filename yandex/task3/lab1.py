import os, sys
import pandas
from sklearn.svm import SVC
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def load_data():
	data_train = pandas.read_csv('./data/svm-data.csv', header=None)
	classes_train, data_train = io_yandex.get_value_column(data_train, 0)
	return data_train, classes_train


def constact_SVC():
	svc = SVC(kernel='linear', C=100000, random_state=241)
	return svc

data_train, classes_train = load_data()
abc = SVC(kernel='linear', C=100000, random_state=241)
#abc.fit(data_train[:20], classes_train[:20])
abc.fit(data_train, classes_train)
print(abc.support_)
vectors = [x+1 for x in abc.support_]
vectors.sort()
io_yandex.print_result(' '.join(map(str, vectors)), "1.txt")