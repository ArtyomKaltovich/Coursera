import os, sys
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import hstack
PACKAGE_PARENT = "../.."
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def load_data(path):
    train = pandas.read_csv(path)
    #train = train.head(100)
    target, train = io_yandex.get_value_column(train, 'SalaryNormalized')
    train['FullDescription'] = train['FullDescription'].str.lower()
    train['FullDescription'] = train['FullDescription'].replace('[^a-z0-9]', ' ', regex = True)
    train['LocationNormalized'].fillna('nan', inplace=True)
    train['ContractTime'].fillna('nan', inplace=True)
    return target, train


target, train = load_data('salary-train.csv')
tfid_vectoriser = TfidfVectorizer(min_df=5)
train_text = tfid_vectoriser.fit_transform(train['FullDescription'])
dict_vectorizer = DictVectorizer()
train_categ = dict_vectorizer.fit_transform(train[['LocationNormalized', 'ContractTime']].to_dict('records'))
train = hstack(blocks=[train_text, train_categ])

clf = Ridge(alpha=1, random_state=241)
clf.fit(train, target)

target, train = load_data('salary-test-mini.csv')
train_text = tfid_vectoriser.transform(train['FullDescription'])
train_categ = dict_vectorizer.transform(train[['LocationNormalized', 'ContractTime']].to_dict('records'))
train = hstack(blocks=[train_text, train_categ])
target = clf.predict(train)
io_yandex.print_result(' '.join(map(io_yandex.two_digit_round, target)), '1.txt')