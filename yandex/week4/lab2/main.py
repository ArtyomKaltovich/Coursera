import os, sys
import pandas
from sklearn.decomposition import PCA
from numpy import corrcoef, argmax
PACKAGE_PARENT = "../.."
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


train = pandas.read_csv('close_prices.csv')
target, train = io_yandex.get_value_column(train, 'date')
#print(train.head(5))

pca = PCA(n_components=10)
pca.fit(train)
ratio = 0.
number = 0
while ratio < 0.9 and number < len(pca.explained_variance_ratio_):
	ratio += pca.explained_variance_ratio_[number]
	number += 1
print(number, ratio)
io_yandex.print_result(str(number), '1_1.txt')

reduced = pca.transform(train)[:,0]

real = pandas.read_csv('djia_index.csv')
real = real['^DJI']
correlation = corrcoef(reduced, real)[0, 1]
io_yandex.print_result(str(correlation), '1_2.txt')

company = train.columns[argmax(pca.components_[0])]
io_yandex.print_result(company, '1_3.txt')
