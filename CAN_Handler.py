from pyvit import can
from pyvit.hw import socketcan
import serial
import struct
import time
import sys
import threading
import json

class canHandler(object):
	def __init__(self):
		self.port_name = "/dev/ttyACM0"
		self.port = None
		self.stop = 0
		self.data = []
		self.frame_counter = 0
		self.data_counter = 0
		self.dev =None

	def open_CAN_connection(self):
		print('Opening CAN socket')
		try:
			self.dev = socketcan.SocketCanDev("can0")
			self.dev.start()
		except:
			print('Could not open SocketCAN port')

	def send_to_can(self,ID,Data):
		frame =can.Frame(ID,Data)
		self.dev.send(frame)
		#print("done")

	def request_CAN_data(self, NODE_ID, num_of_values):
		counter = 0
		
		while True:
			if self.stop:
				break
			counter = counter + 1
			if counter == 1:
				print('heartbeat')
				counter = 0
				for value in range(45):
					if self.stop:
						break
					frame =can.Frame(NODE_ID,[0,0,0,0,(value+3)])
					self.dev.send(frame)
					#time.sleep(0.001)
			time.sleep(1)

	def read_from_CAN(self):
		Rx_data = self.dev.recv()
		return Rx_data


	def decode_float(self,data_ID, data_frame):
		json3 = {}
		#print(data_ID)
		if data_ID == 1792:
			(value,) = struct.unpack('>B', bytes({data_frame[4]}))
       
			data = bytes({data_frame[3]})
			data += (bytes({data_frame[2]}))
			data += (bytes({data_frame[1]}))
			data += (bytes({data_frame[0]}))
			
			#print(value,float_out)

			if value == 4:
				(float_out,) = struct.unpack('>f', data)
				json3["VT"] = round(float_out,2)
				#print("DATA!")
			elif value == 5:
				(float_out,) = struct.unpack('>f', data)
				json3["I"] = round(float_out,1)	
			elif value == 6:
				(float_out,) = struct.unpack('>f', data)
				json3["Vcl"] = round(float_out,3)
			elif value == 7:
				(float_out,) = struct.unpack('>f', data)
				json3["Vcln"] = round(float_out,0)	
			elif value == 8:
				(float_out,) = struct.unpack('>f', data)
				json3["Vch"] = round(float_out,3)
			elif value == 9:
				(float_out,) = struct.unpack('>f', data)
				json3["Vchn"] = round(float_out,0)
			elif value == 10:
				(float_out,) = struct.unpack('>f', data)
				json3["Va"] = round(float_out,3)
			elif value == 11:
				(float_out,) = struct.unpack('>f', data)
				json3["Thc"] = round(float_out,3)
			elif value == 12:
				(float_out,) = struct.unpack('>f', data)
				json3["Thcn"] = round(float_out,0)
			elif value == 13:
				(float_out,) = struct.unpack('>f', data)
				json3["Tlc"] = round(float_out,3)
			elif value == 14:
				(float_out,) = struct.unpack('>f', data)
				json3["Tlcn"] = round(float_out,0)
			elif value == 15:
				(float_out,) = struct.unpack('>f', data)
				json3["Ta"] = round(float_out,3)
			elif value == 16:
				(float_out,) = struct.unpack('>f', data)
				json3["Vx"] = round(float_out,3)
			elif value == 17:
				(float_out,) = struct.unpack('>f', data)
				json3["SOC"] = round(float_out,0)

				
			elif value == 18:
				(float_out,) = struct.unpack('>f', data)
				json3["RIa"] = round(float_out,3)
			elif value == 19:
				(float_out,) = struct.unpack('>f', data)
				json3["RIh"] = round(float_out,3)
			elif value == 20:
				(float_out,) = struct.unpack('>f', data)
				json3["RIhcn"] = round(float_out,0)	
			elif value == 21:
				(float_out,) = struct.unpack('>f', data)
				json3["V0"] = round(float_out,3)
			elif value == 22:
				(float_out,) = struct.unpack('>f', data)
				json3["V1"] = round(float_out,3)
			elif value == 23:
				(float_out,) = struct.unpack('>f', data)
				json3["V2"] = round(float_out,3)
			elif value == 24:
				(float_out,) = struct.unpack('>f', data)
				json3["V3"] = round(float_out,3)
			elif value == 25:
				(float_out,) = struct.unpack('>f', data)
				json3["V4"] = round(float_out,3)
			elif value == 26:
				(float_out,) = struct.unpack('>f', data)
				json3["V5"] = round(float_out,3)
			elif value == 27:
				(float_out,) = struct.unpack('>f', data)
				json3["V6"] = round(float_out,3)
			elif value == 28:
				(float_out,) = struct.unpack('>f', data)
				json3["V7"] = round(float_out,3)
			elif value == 29:
				(float_out,) = struct.unpack('>f', data)
				json3["V8"] = round(float_out,3)
			elif value == 30:
				(float_out,) = struct.unpack('>f', data)
				json3["V9"] = round(float_out,3)
			elif value == 31:
				(float_out,) = struct.unpack('>f', data)
				json3["V10"] = round(float_out,3)
			elif value == 32:
				(float_out,) = struct.unpack('>f', data)
				json3["V11"] = round(float_out,3)
			elif value == 33:
				(float_out,) = struct.unpack('>f', data)
				json3["V12"] = round(float_out,3)
			elif value == 34:
				(float_out,) = struct.unpack('>f', data)
				json3["V13"] = round(float_out,3)
			elif value == 35:
				(float_out,) = struct.unpack('>f', data)
				json3["V14"] = round(float_out,3)
			elif value == 36:
				(float_out,) = struct.unpack('>f', data)
				json3["T0"] = round(float_out,1)
			elif value == 37:
				(float_out,) = struct.unpack('>f', data)
				json3["T1"] = round(float_out,1)
			elif value == 38:
				(float_out,) = struct.unpack('>f', data)
				json3["T2"] = round(float_out,1)
			elif value == 39:
				(float_out,) = struct.unpack('>f', data)
				json3["T3"] = round(float_out,1)
			elif value == 40:
				(float_out,) = struct.unpack('>f', data)
				json3["T4"] = round(float_out,1)
			elif value == 41:
				(float_out,) = struct.unpack('>f', data)
				json3["T5"] = round(float_out,1)
			elif value == 42:
				(float_out,) = struct.unpack('>f', data)
				json3["T6"] = round(float_out,1)
			elif value == 43:
				(float_out,) = struct.unpack('>f', data)
				json3["T7"] = round(float_out,1)
			elif value == 44:
				(float_out,) = struct.unpack('>f', data)
				json3["T8"] = round(float_out,1)
			elif value == 45:
				(float_out,) = struct.unpack('>f', data)
				json3["T9"] = round(float_out,1)
			elif value == 46:
				(float_out,) = struct.unpack('>f', data)
				json3["T10"] = round(float_out,1)
			elif value == 47:
				(float_out,) = struct.unpack('>f', data)
				json3["T11"] = round(float_out,1)
			elif value == 48:
				(float_out,) = struct.unpack('>f', data)
				json3["T12"] = round(float_out,1)
			elif value == 49:
				(float_out,) = struct.unpack('>f', data)
				json3["T13"] = round(float_out,1)
			elif value == 50:
				(float_out,) = struct.unpack('>f', data)
				json3["T14"] = round(float_out,1)
			elif value == 51:
				(float_out,) = struct.unpack('>f', data)
				json3["T15"] = round(float_out,1)
				print("T15 = "+ str(float_out))
			elif value == 52:
				(float_out,) = struct.unpack('>I', data)
				json3["Status"] = round(float_out,1)
				print("Status = "+ str(float_out))
			else:
				return None

			json2 = json.dumps(json3)
			return json2

		elif data_ID == 1553:

			(status,) = struct.unpack('>B', bytes({data_frame[4]}))
			data = bytes({data_frame[2]})
			data += (bytes({data_frame[3]}))
			(short_C,) = struct.unpack('>h', data)
			current = float(short_C)/10
			json3["CHG_I"] = round(current,2)
			data = (bytes({data_frame[0]}))
			data += (bytes({data_frame[1]}))
			(short_V,) = struct.unpack('>h', data)
			voltage = float(short_V)/10
			json3["CHG_V"] = round(voltage,2)
			json3["CHG_status"] = status
			json2 = json.dumps(json3)
			#print(json2)
			return json2		
		else:
			return None


	def close_CAN_connection(self):
		self.dev.stop()
		

if __name__ == '__main__':
	try:
		if len(sys.argv) == 1:
			print("Please supply command line argumemnt as follows:\n")
			print("1: Test UART connection to CAN shield, simple value send\n")
			print("2: Full serial test, request values and print received values\n")
		elif sys.argv[1] == "1":
			print('hello1')
			myCAN = canHandler()
			myCAN.open_CAN_connection()
			print(myCAN.read_from_CAN())
##			for i in range(10):
##				print(myCAN.read_from_CAN())
##				myCAN.send_to_can(0x1,[0,0,0,0,10])
##				x = myCAN.read_from_CAN()
##				print(myCAN.decode_float(x.data))
##				time.sleep(1)
		elif sys.argv[1] == "2":
			print('hello2')
			myCAN = canHandler()
			myCAN.open_CAN_connection()
			#request_thread = threading.Thread(target = myCAN.request_CAN_data, args = (NODE_ID, NUM_VALUES))
			#request_thread.start()
			while True:
				data = myCAN.read_from_CAN()
				
				decoded_data = myCAN.decode_float(data.arb_id, data.data)
				print(decoded_data)

	except KeyboardInterrupt:
		print('Keyboard interrupt')
	except:
		print('Error', sys.exc_info()[0], sys.exc_info()[1], 'on line ', sys.exc_info()[2])
	finally:
		if myCAN != None:
			myCAN.stop = 1
			myCAN.close_CAN_connection()
			#request_thread.join()
