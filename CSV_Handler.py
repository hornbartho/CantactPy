import csv
import glob
import datetime
import os

class CSVHandler(object):
	def __init__(self, index):
		self.logfile = None
		self.logwriter = None
		self.index = index
		self.counter = 0
		self.folder_path = None
		self.filename = None

	def create_CSV_file(self):
		print('create CSV for index ' + self.index)
		self.folder_path = '/var/log/python/'
		if not os.path.isdir(self.folder_path):
			os.makedirs(self.folder_path)

		self.filename = self.folder_path + self.index
		self.logfile = open(self.filename, 'ab')
		self.logwriter = csv.writer(self.logfile, dialect = 'excel')

	def write_line(self,Telemset):
		self.counter += 1
		if self.counter > 100000:
			self.counter = 0
			self.close_CSV()
			self.create_CSV_file()
		self.logwriter.writerow(Telemset)

	def is_empty_file(self):
		if os.stat(self.filename).st_size == 0:
			return 1
		else:
			return 0

	def is_empty_dir(self):
		if not os.listdir(self.folder_path):
			return 1
		else:
			return 0

	def close_CSV(self):
		self.logfile.close()
		if self.is_empty_file():
			print('Empty file, deleting ' + self.filename)
			os.remove(self.filename)
		if self.is_empty_dir():
			os.rmdir(self.folder_path)

if __name__ == "__main__":
	myCSV = CSVHandler('BMS')
	myCSV.create_CSV_file()
	myCSV.close_CSV()
	
