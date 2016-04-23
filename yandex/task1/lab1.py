import pandas, numpy, scipy.stats

def get_procent(dataframe, colomn_name, value):
	s = dataframe.loc[dataframe[colomn_name] == value]
	s = float(len(s.index)) / float(len(dataframe.index)) * 100
	s = two_digit_round(s)
	return s


def print_result(s, file_name):
	print (s)
	with open(file_name, "w") as text_file:
	    text_file.write(s)


def two_digit_round(s):
	return "{0:.2f}".format(s)

data = pandas.read_csv('titanic.csv', index_col='PassengerId')
print (list(data.columns.values))

s = data['Sex'].value_counts()
s = str(s[0]) + ' ' + str(s[1])
print_result(s, '1.txt')

s = get_procent(data, 'Survived', 1)
print_result(s, '2.txt')

s = get_procent(data, 'Pclass', 1)
print_result(s, '3.txt')

s = data.loc[data.Age.notnull()]
s = s['Age']
s = str(two_digit_round(float(numpy.mean(s, axis = 0)))) + ' ' \
	 + str(two_digit_round(float(numpy.median(s, axis = 0))))
print_result(s, '4.txt')

s = scipy.stats.pearsonr(data['SibSp'], data['Parch'])
s = two_digit_round(s[0])
print_result(s, '5.txt')

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
print_result(grouped.Name.iloc[0], '6.txt')