import pandas


def load_titanic_to_dataframe():
	data = pandas.read_csv('../data/titanic.csv', index_col='PassengerId')
	return data


def load_wine_to_dataframe():
	data = pandas.read_csv('../data/wine.data', header=None)
	return data


def print_result(s, file_name):
    print (s)
    with open(file_name, "w") as text_file:
        text_file.write(s)


def three_digit_round(s):
    return "{0:.3f}".format(s)


def two_digit_round(s):
    return "{0:.2f}".format(s)


def one_digit_round(s):
    return "{0:.1f}".format(s)


def get_value_column(df, column_name):
    column = df[column_name]
    df = df.drop(column_name, axis=1)
    return column, df