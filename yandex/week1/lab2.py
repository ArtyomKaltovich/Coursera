import os, sys
import pandas
from sklearn import tree
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex


def prepare_data(df):
    df = df.drop(df.columns[[2, 5, 6, 7, 9, 10]], axis=1)
    df = df.dropna()
    df['Sex'] = df['Sex'].map({'female': 0., 'male': 1.}) # replace sex string by 1 or 0. 1 is male (this is obvious :) )
    return df


def create_decision_tree(dataframe, value_column):
    clf = tree.DecisionTreeClassifier(random_state=241)
    return clf.fit(dataframe, value_column) 


def calculate_most_important_value(df, importances):
    first = [0, 0]     #index value
    second = [0, 0]    #index value
    index = 0
    for value in importances:
        if value > first[1]:
            second = first
            first = [index, value]
        elif value > second[1]:
            second = [index, value]
        index += 1
    result = df.columns[first[0]] + ' ' + df.columns[second[0]]
    io_yandex.print_result(result, "1b.txt")


df = io_yandex.load_titanic_to_dataframe()  
df = prepare_data(df)
is_survived, df = io_yandex.get_value_column(df,'Survived')
clf = create_decision_tree(df, is_survived)
importances = clf.feature_importances_
print(importances)
calculate_most_important_value(df, importances) #Fare Sex
