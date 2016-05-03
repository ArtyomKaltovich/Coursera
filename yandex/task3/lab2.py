import os, sys
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


newsgroups = datasets.fetch_20newsgroups(
                    subset='all', 
                    categories=['alt.atheism', 'sci.space']
             )

vectoriser = TfidfVectorizer()
train = vectoriser.fit_transform(newsgroups.data, newsgroups.target)
feature_mapping = vectoriser.get_feature_names()
#print (feature_mapping)
#grid = {'C': numpy.power(10.0, numpy.arange(-5, 6))}
grid = {'C': numpy.power(10.0, numpy.arange(1, 2))}
cv = KFold(len(newsgroups.data), n_folds=5, shuffle=True, random_state=241)
clf = SVC(kernel='linear', random_state=241)
gs = GridSearchCV(clf, grid, scoring='accuracy', cv=cv)
gs.fit(train, newsgroups.target)
print(gs.coef_)
for a in gs.grid_scores_:
    print(a.mean_validation_score) # — оценка качества по кросс-валидации
    print(a.parameters) # — значения параметров