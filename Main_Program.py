from Master_Handler import MasterHandler
from CAN_Handler import canHandler

# Serial imports
import serial
import time
import sys

NODE_ID = 1
NUM_VALUES_BMS = 40						# 49 BMS and 3 Charger = 52 Values
INDEXES = ['bms','charger','gps']
BMS = 0
CHARGER = 1
GPS = 2
START_BYTE = '\xfe'

def create_printout(data):
	printout = []
	for i in range(len(myMaster.telemset_bms)):
		if i == 0:
			printout = [myMaster.telemset_bms[i]]
		else:
			printout.append(['%.3f' % myMaster.telemset_bms[i]])
	return printout



if __name__ == "__main__":
	time.sleep(0.5)
	try:
		myMaster = MasterHandler(NODE_ID, NUM_VALUES_BMS)
		myMaster.initialise_handlers()
		#myMaster.start_request_thread()
		myMaster.start_gps_thread()

		while True:
			CAN_data = myMaster.can.read_from_CAN()
			decoded_CAN_data = myMaster.can.decode_float(CAN_data.arb_id, CAN_data.data)
			if decoded_CAN_data != None:

#####################
##                                index = myMaster.which_index(number)
##                                myMaster.add_data_to_index(number, data, index)
##                                if myMaster.is_last_in_index(number, index):
##                                        myMaster.log_telemset(index)
##                                        number= 0
##                                        data5  = 0
#####################
				
				#print(decoded_CAN_data)
				myMaster.Mqtt_Client.publish(decoded_CAN_data)
				#print(myMaster.Mqtt_Client.status)

			if myMaster.queue.empty() == False:
				gps_data = myMaster.queue.get()
				myMaster.Mqtt_Client.publish(gps_data)
				print(gps_data)
##			# read data
##			if myMaster.serial.port.inWaiting():
##				value= myMaster.serial.read_from_UART(1)
##				if value== START_BYTE:	
##					data_frame = myMaster.serial.read_dataframe()
##				
##					if myMaster.serial.is_valid(data_frame):
##						[number, data] = myMaster.serial.decode_dataframe(data_frame)
##						#print number, data
##						index = myMaster.which_index(number)
##						myMaster.add_data_to_index(number, data, index)
##						if myMaster.is_last_in_index(number, index):
##							if myMaster.is_complete_telemset(index):
##								printout = create_printout(myMaster.telemset_bms)
##								print printout
##								#for i in range(5):
##								
##                                                                myMaster.Mqtt_publish(index)
##
##                                                                #myMaster.telemset_bms
##								myMaster.log_telemset(index)
##								number= 0
##								data = 0
##							else:
##								print 'Incomplete dataset'
##					else:
##						print "Invalid data frame"
##				else:
##					print "Invalid start byte"
##
	except serial.SerialException:
		print("Serial exception")
		
	except KeyboardInterrupt:
		print("Keyboard interrupt")

	except:
		print("Main thread error:", sys.exc_info()[0], sys.exc_info()[1], "on line ", sys.exc_info()[2].tb_lineno)
		
	finally:
		print('Closing all')
		myMaster.close_all()
