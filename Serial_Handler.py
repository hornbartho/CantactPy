import RPi.GPIO as GPIO
import serial
import struct
import time
import sys
import threading

START = '\xfe'
NODE_ID = 1
DATA = ['\x00', '\x00', '\x00', '\x00']
STOP = '\xff'
NUM_VALUES = 24 		#20->24

class SerialHandler(object):
	def __init__(self):
		self.port_name = "/dev/ttyS1"
		self.baudrate = 117200
		self.port = None
		self.stop = 0
		self.dataframe = []
		self.data = 0
		self.frame_counter = 0
		self.data_counter = 0

	def open_serial_connection(self):
		print 'Opening CAN serial port'
		try:
			self.port = serial.Serial(self.port_name, baudrate=self.baudrate)
			self.port.close()
			self.port = serial.Serial(self.port_name, baudrate=self.baudrate)
		except:
			print 'Could not open CAN serial port'

	def send_request(self, NODE_ID, num_of_values):
		print 'Serial request thread'

		loop_time = time.time() - 600
		counter = 0
		while True:
			if self.stop:
				break
			counter += 1
			if counter > 5:
				print 'heartbeat'
				counter = 0
			for value in range(num_of_values):
				if self.stop:
					break
				data_frame = [START, chr(NODE_ID), chr(value+1)] + DATA + [STOP]
				for i in range(8):
					self.port.write(data_frame[i])
					time.sleep(0.015)
			time.sleep(4)
		print "done"

	def read_from_UART(self, num_of_values):
		for i in range(num_of_values):
			Rx_data = self.port.read(num_of_values)
		return Rx_data

	def read_dataframe(self):
		data_frame = ""
		data_frame += '\xfe'
		data_frame_counter = 0
		while data_frame_counter < 7:  # read rest of frame
			if self.port.inWaiting():
				data = self.read_from_UART(1)
				data_frame += data
				data_frame_counter += 1
		return data_frame


	def is_valid(self,data_frame):
		# Dataframe should have format:
		# START | ID | VALUE | DATA | STOP
		valid = 0
		if data_frame[0] == '\xfe':		# START byte
			if data_frame[7] == '\xff':	# STOP byte
				if data_frame[1] == '\x01':	# Slave CAN shield
					#if (data_frame[2] < 21 and data_frame[2] > 0):
						# VALUE byte between 1 and 20
					valid = 1
		return valid

	def decode_dataframe(self, data_frame):
		#value,) = struct.unpack('>B', data_frame[2])
		(value,) = struct.unpack('>B', data_frame[2])
		data = ''
		data += data_frame[3]
		data += data_frame[4]
		data += data_frame[5]
		data += data_frame[6]
		(float_out,) = struct.unpack('>f', data)
		return value,float_out

	def check_all_values(self,Telemset, None_value):
		got_all_values = 1
		for i in range(len(Telemset)):
			if Telemset[i] == None_value:
				got_all_values = 0
		return got_all_values

	def close_serial_connection(self):
		self.port.reset_input_buffer()
		self.port.close()

if __name__ == '__main__':
	try:
		mySerial = None
		if len(sys.argv) == 1:
			print "Please supply command line argumemnt as follows:\n"
			print "1: Test UART connection to CAN shield, simple value send\n"
			print "2: Full serial test, request values and print received values\n"
		elif sys.argv[1] == "1":
			mySerial = SerialHandler()
			mySerial.open_serial_connection()
			for i in range(10):
				mySerial.port.write(chr(i))
				time.sleep(1)
		elif sys.argv[1] == "2":  
			mySerial = SerialHandler()
			mySerial.open_serial_connection()
			request_thread = threading.Thread(target = mySerial.send_request, args = (NODE_ID, NUM_VALUES))
			request_thread.start()
			while True:
				if mySerial.port.inWaiting():
					value = mySerial.read_from_UART(1)
					if value == START:
						data_frame = mySerial.read_dataframe()
						if mySerial.is_valid(data_frame):
							[number, data] = mySerial.decode_dataframe(data_frame)
							print number, data
	except serial.SerialException:
		print 'Serial exception'
	except KeyboardInterrupt:
		print 'Keyboard interrupt'
	except:
		print 'Error', sys.exc_info()[0], sys.exc_info()[1], 'on line ', sys.exc_info()[2]
	finally:
		if mySerial != None:
			mySerial.stop = 1
			request_thread.join()
			mySerial.close_serial_connection()

