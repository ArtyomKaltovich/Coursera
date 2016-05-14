import os, sys
import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold, cross_val_score
from numpy import mean
import time

PACKAGE_PARENT = "../.."
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def replace_sex(x):
	if x == 'M':
		return 1
	elif x == 'I':
		return 0
	elif x == 'F':
		return -1


def load_data(path):
    train = pandas.read_csv(path)
    #train = train.head(100)
    target, train = io_yandex.get_value_column(train, 'Rings')
    train['Sex'] = list(map(replace_sex, train['Sex']))
    return train, target


X, y = load_data('abalone.csv')
start = time.time()
for i in range(1, 51):
	clf = RandomForestRegressor(n_estimators=i, random_state=1)
	kf = KFold(len(y), n_folds=5, random_state=1, shuffle=True)
	score = mean(cross_val_score(clf, X, y, cv=kf, scoring='r2', n_jobs=-1))
	#print(i, score) 
	if (score > 0.52):
		io_yandex.print_result(str(i), "1.txt")
		break
end = time.time()
print(end - start)