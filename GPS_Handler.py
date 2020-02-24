import serial
from serial import Serial
from serial import SerialException
import pynmea2
import sys
import time
import numpy as np
import json
import geohash2 as Geohash
import os
import queue as queue

from rfc3339 import rfc3339
from datetime import datetime

class GPSHandler(object):
	def __init__(self, logging=None, CSV=None):
		self.stop = 0
		self.counter = 0
		self.port = serial.Serial('/dev/ttyACM0', 115200)
		#self.logging = logging
		#self.CSV = CSV

	def read_gps(self, q):
		try:
			print("Connecting GPS")
			json3 = {}
			while True:
				if not self.stop:
					line = self.port.readline()
					#print(line)
					line = line.decode('utf-8')
					if(line[3:6] == 'VTG'): # $GPVTG
						msgVTG = pynmea2.parse(line)
						json3["V"] = msgVTG.spd_over_grnd_kmph

					if(line[3:6] == 'GGA'): # $GPGGA
						msgGGA = pynmea2.parse(line)
						if msgGGA.gps_qual >= 1: 
							
							json3["Latitude"] = round(msgGGA.latitude, 5)
							json3["Longitude"] = round(msgGGA.longitude, 5)
							json3["Altitude"] = round(msgGGA.altitude, 5)
							json3["Satellites"] = msgGGA.num_sats
							json_string2 = json.dumps(json3)
							
							json3 = {}
							#print(json_string2)
							if not q.full():
								q.put(json_string2)
							
						elif msgGGA.gps_qual == 0:
							print('GPS not connected:')
				else:
					print("GPS thread stopping")
					break
		except SerialException:
			print('GPS thread - Serial Exception')
		except:
			print('GPS thread - Error', sys.exc_info()[0], sys.exc_info()[1])
		finally:
			self.close_port()

	def close_port(self):
		self.port.close()
		print('Closing GPS port')

if __name__ == '__main__':
	q = queue.Queue(20)
	myGPS = GPSHandler()
	try:
		myGPS.read_gps(q)
	
	except KeyboardInterrupt:
		print("KeyboardInterrupt")

	except:
		print("Error:", sys.exc_info()[0], sys.exc_info()[1])
	
	finally:
		myGPS.stop = 1
