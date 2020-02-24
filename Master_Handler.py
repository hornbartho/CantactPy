from CAN_Handler import canHandler
#from Logging_Handler import LoggingHandler
#from CSV_Handler import CSVHandler
from GPS_Handler import GPSHandler

from Mqtt_Handler import MyMQTTClass

from rfc3339 import rfc3339
from datetime import datetime

import queue as queue

import datetime
import threading
import time
import numpy as np
import socket

BMS = 0
CHARGER = 1
filtr = 0

class MasterHandler(object):
	def __init__(self, NODE_ID, NUM_VALUES):
		self.node_id = NODE_ID
		self.num_values = NUM_VALUES
		self.request_thread = None
		self.null_counter = 0
		self.can= canHandler()
		#self.logging = LoggingHandler()
		#self.CSV_bms = CSVHandler("bms")
		#self.telemset_bms = []
		#self.CSV_gps = CSVHandler("gps")
		self.gps = GPSHandler()

		self.gps_thread = None
		self.queue = queue.Queue(20)
		#self.CSV_charger = CSVHandler("charger")
		#self.telemset_charger = []

		self.Mqtt_Client = MyMQTTClass("\""+ socket.gethostname() + "\"")

	def initialise_handlers(self):
		self.can.open_CAN_connection() 
		#self.logging.create_rsyslog_handler()
		#self.CSV_bms.create_CSV_file()
		#self.CSV_gps.create_CSV_file()
		#self.CSV_charger.create_CSV_file()
		#self.telemset_charger.append(rfc3339(time.time()))
		#print self.telemset_charger
		#self.telemset_charger = [rfc3339(time.time()), 0 , 0 , 0]
		#print self.telemset_charger
		#self.telemset_bms.append(rfc3339(time.time()))
		
		self.Mqtt_Client.run()	
				      
	def start_request_thread(self):
		self.request_thread = threading.Thread(target = self.can.request_CAN_data, args = (self.node_id, self.num_values))
		self.request_thread.start()
  
	def start_gps_thread(self):
		self.gps_thread = threading.Thread(target = self.gps.read_gps, args = (self.queue,))
		#self.gps_thread.daemon = True
		self.gps_thread.start()

	def which_index(self, number):
		if ((number >= 1) and (number <= 3)):
			index = CHARGER
		elif ((number >= 4) and (number <= 52)):			#Changed from 17 to 52
			index = BMS
		return index



##	def log_telemset(self, index):
##		global filtr
##		if index == BMS:
##			data_string = self.logging.create_bms_log_string(self.telemset_bms)
##			self.logging.write_log_entry(data_string)
##			self.CSV_bms.write_line(self.telemset_bms)
##			self.telemset_bms = []
##			arraytemp = [rfc3339(time.time()),99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99]
##                                                			#Changed from 14 to 49
##                        self.telemset_bms = arraytemp
##			#self.telemset_bms.append(rfc3339(time.time()))
##			#self.telemset_bms.append(99*np.zeros(49))					#Chnaged from 14 to 49
##                        
##
##
##		elif index == CHARGER:
##			filtr = filtr + 1
##			if filtr == 5:
##				data_string = self.logging.create_charger_log_string(self.telemset_charger)
##				self.logging.write_log_entry(data_string)
##				self.CSV_charger.write_line(self.telemset_charger)
##				self.telemset_charger = []
##				#self.telemset_charger.append(rfc3339(time.time())) #str(datetime.now()))
##				#self.telemset_charger.append(np.ones(3))
##				self.telemset_charger = [rfc3339(time.time()), 0 , 0 , 0]
##				filtr = 0


	def close_all(self):
		#print('Stopping CAN thread')
		#self.can.stop = 1
		#self.request_thread.join()

		print('Closing CAN port')
		self.can.close_CAN_connection()

		print('Stopping GPS thread')
		self.gps.stop = 1
		self.gps_thread.join()
		self.gps.close_port()

#		print 'Closing output files'
#		self.CSV_bms.close_CSV()
#		self.CSV_gps.close_CSV()
#		self.CSV_charger.close_CSV()

		print('Closing MQTT client')
		self.Mqtt_Client.close()

