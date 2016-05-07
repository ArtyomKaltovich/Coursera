import pandas, numpy, scipy.stats, os, sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from mylib import io_yandex

def get_procent(dataframe, colomn_name, value):
    s = dataframe.loc[dataframe[colomn_name] == value]
    s = float(len(s.index)) / float(len(dataframe.index)) * 100
    s = io_yandex.two_digit_round(s)
    return s


data = io_yandex.load_titanic_to_dataframe()
print (list(data.columns.values))
len(df.index)
s = data['Sex'].value_counts()
s = str(s[0]) + ' ' + str(s[1])
io_yandex.print_result(s, '1.txt')

s = get_procent(data, 'Survived', 1)
io_yandex.print_result(s, '2.txt')

s = get_procent(data, 'Pclass', 1)
io_yandex.print_result(s, '3.txt')

s = data.loc[data.Age.notnull()]
s = s['Age']
s = str(io_yandex.two_digit_round(float(numpy.mean(s, axis = 0)))) + ' ' \
     + str(io_yandex.two_digit_round(float(numpy.median(s, axis = 0))))
io_yandex.print_result(s, '4.txt')

s = scipy.stats.pearsonr(data['SibSp'], data['Parch'])
s = io_yandex.two_digit_round(s[0])
io_yandex.print_result(s, '5.txt')

s = data.loc[data['Sex'] == 'female']
s = s['Name']
l = []
for row in s:
    index = row.find('(')
    if index > -1:
        row = row[index + 1:]
    index = row.find('Miss.')
    if index > -1:
        row = row[index + len('Miss.') + 1:]
    index = row.find('Mrs.')
    if index > -1:
        row = row[index + len('Mrs.') + 1:]
    index = row.find('Mlle.')
    if index > -1:
        row = row[index + len('Mrs.') + 1:]
    index = row.find(' ')
    if index > -1:
        row = row[:index]
    index = row.find(')')
    if index > -1:
        row = row[:index]
    l.append(row)
new_data = pandas.DataFrame(l, columns = ['Name'])
#grouped = new_data.groupby('Name').count()
grouped = pandas.DataFrame({'count' : new_data.groupby( ['Name'] ).size()}).reset_index().sort_values('count', ascending=False)
#print(new_data['Name'].value_counts())
io_yandex.print_result(grouped.Name.iloc[0], '6.txt')