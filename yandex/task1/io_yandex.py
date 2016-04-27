import pandas


def load_titanic_to_dataframe():
	data = pandas.read_csv('../titanic.csv', index_col='PassengerId')
	return data


def print_result(s, file_name):
    print (s)
    with open(file_name, "w") as text_file:
        text_file.write(s)