import os, sys
import heapq, itertools
import pandas
import sklearn
import numpy
from sklearn import datasets
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def n_largest_index(a,N):
    return numpy.argsort(a)[::-1][:N]

def get_key_words(vectoriser, coef_data, N):
	key_words = []
	feature_mapping = vectoriser.get_feature_names()
	for i in n_largest_index(coef_data, N):
		key_words.append(feature_mapping[i])
	return key_words

newsgroups = datasets.fetch_20newsgroups(
                    subset='all', 
                    categories=['alt.atheism', 'sci.space']
             )

vectoriser = TfidfVectorizer()
train = vectoriser.fit_transform(newsgroups.data).toarray()
#grid = {'C': numpy.power(10.0, numpy.arange(-5, 6))}
#cv = KFold(len(newsgroups.data), n_folds=5, shuffle=True, random_state=241)
#clf = SVC(kernel='linear', random_state=241)
#gs = GridSearchCV(clf, grid, scoring='accuracy', cv=cv)
#gs.fit(train, newsgroups.target)
#print(gs.best_estimator_.coef_)
#coef = gs.best_estimator_.coef_
#coef_data = numpy.abs(coef.data)
#coef_class = numpy.abs(coef.class)
#key_words = get_key_words(vectoriser, coef_data, 10)
#key_words.sort()
#print(gs.best_params_['C'])
#for a in gs.grid_scores_:
#    print(a.mean_validation_score) # — оценка качества по кросс-валидации
#    print(a.parameters) # — значения параметров
clf = SVC(kernel='linear', C=1., random_state=241) # C > 1 - best values
clf.fit(train, newsgroups.target)
coef = clf.coef_
coef_data = numpy.abs(coef.data)[0]
print(coef_data)
key_words = get_key_words(vectoriser, coef_data, 10)
key_words.sort()
io_yandex.print_result(','.join(map(str, key_words)), "1_2.txt")