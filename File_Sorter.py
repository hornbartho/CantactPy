import glob
import shutil
import os

folders = ["bms", "gps"]
num = 0
for folder in folders:
	print folder
	for month in range(3,5):
		print month
		for i in range(0,32):
			print i
			if i<10:
				globs = '/home/mellow/Documents/output_files/' + folder + '_2017-0' + str(month) +'-0' + str(i) + '*'
			else:
				globs = '/home/mellow/Documents/output_files/' + folder + '_2017-0' + str(month) +'-' + str(i) + '*'

			print globs
			files = glob.glob(globs)
			num += len(files)
			print files
			filepath = '/home/mellow/Documents/output_files1/' + folder + '/' + '2017-0' + str(month) +'-' + str(i) + '/'
			for file in files:
				if not os.path.isdir(filepath):
					os.makedirs(filepath)
				shutil.copy2(file, filepath)

print 'sorted: ' + str(num)
print ' out of: ' + str(len(glob.glob('/home/mellow/Documents/output_files/*')) - len(folders))