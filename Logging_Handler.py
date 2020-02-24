import logging
import logging.handlers
import json

import sys
from rfc3339 import rfc3339
import time
class LoggingHandler(object):
	def __init__(self):
		self.logger = logging.getLogger('Python')
		self.logger.setLevel(logging.INFO)

	def create_file_handler(self):
		handler_file = logging.FileHandler('PythonLog.log')
		self.logger.addHandler(handler_file)

	def create_rsyslog_handler(self):
		handler_rsyslog = logging.handlers.SysLogHandler('/dev/log')
		self.logger.addHandler(handler_rsyslog)

	def write_log_entry(self, message):
		self.logger.info(message)

	def create_bms_log_string(self, data):
		json3 = {}
		json3["m_t"] = data[0]
		json3["d_t"] = "BMS"
		json3["tag"] = "Python"
		for i in range(16):
			if i == 0:
				pass
			else:
				json3["V" + str(i)] = round(data[i],3)
		json3["VT"] = sum(data[1:16])
		#json3["min_voltage"] = min(data[1:16])
		#json3["max_voltage"] = max(data[1:16])
		#json3["ave_voltage"] = sum(data[1:16])/len(data[1:16])

		json3["I"] = round(data[16],3)
		json3["T1"] = round(data[17], 3)
		json3["T2"] = round(data[18],3)
		json3["T3"] = round(data[19],3)
		json3["A_V"] = round(data[20],3)
		json3["R_Avg"] = round(data[21],3)					#Internal Resistance Average
		json3["R_Max"] = round(data[22],3)					#Internal Resistance Max
		json3["R_Cell"] = round(data[23],3)					#Internal Resistance Cell
		json3["SOC"] = round(data[24],2)					#SOC
		#json3["AveTemp"] =  sum(data[17:])/3

		json_string = json.dumps(json3)
		json2 = "{\"message\":" + json_string
		return json2

	def create_charger_log_string(self, data):
		json3 = {}
		json3["m_t"] =  data[0]
		json3["d_t"] = "charger"
		json3["tag"] = "Python"

		json3["CV"] = round(data[1], 3)
		json3["CC"] = round(data[2], 3)
		json3["CS"] = round(data[3], 3)

		json_string = json.dumps(json3)
		json2 = "{\"message\":" + json_string
		return json2

if __name__ == '__main__':
	myLogger = LoggingHandler()
	myLogger.create_rsyslog_handler()
	
	json3 = {}
	if len(sys.argv) > 1:
		json3['extra'] = sys.argv[1]
	json3["measure_time"] =  rfc3339(time.time())
	json3["data_input_type"] = "test"
	json3["tag"] = "Python"

	json_string = json.dumps(json3)
	json2 = "{\"message\":" + json_string

	myLogger.write_log_entry(json2)
