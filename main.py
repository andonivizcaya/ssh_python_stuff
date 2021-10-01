import csv


def read_file(file_name):
	for row in open(file_name, 'r'):
		yield row
