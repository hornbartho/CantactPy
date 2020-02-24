# Copyright (c) 2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution. 
#
# The Eclipse Distribution License is available at 
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# This example shows how you can use the MQTT client in a class.
import sys
import paho.mqtt.client as mqtt
import time
import socket

THINGSBOARD_HOST = '192.168.88.24'
ACCESS_TOKEN = 'mellowcab12'
#client = mqtt.Client()
#client.username_pw_set(ACCESS_TOKEN)
#client.connect(THINGSBOARD_HOST,1883,60)

	
class MyMQTTClass:
	def __init__(self, clientid):
		self._mqttc = mqtt.Client(clientid)
		self._mqttc.on_message = self.mqtt_on_message
		self._mqttc.on_connect = self.mqtt_on_connect
		self._mqttc.on_disconnect = self.mqtt_on_disconnect
		self._mqttc.on_publish = self.mqtt_on_publish
		self._mqttc.on_subscribe = self.mqtt_on_subscribe
		self.Connected = False
		self.status = 'normal'
		
	def mqtt_on_connect(self, mqttc, obj, flags, rc):
		if rc == 0: 
			print("Connected to broker")
			self.Connected = True                #Signal connection
			self._mqttc.subscribe('v1/devices/me/attributes', qos = 1) 
		#print("rc: "+str(rc))
	def mqtt_on_disconnect(self,client,userdata,rc):
		self.Connected = False
		print("Disconnected")
	
	def mqtt_on_message(self, mqttc, obj, msg):
		if str(msg.payload) == 'normal':
		       self.status = 'normal'
		elif str(msg.payload) == 'debug':
		       self.status = 'debug'
		elif str(msg.payload) == 'saver':
		       self.status = 'saver'
		print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
	def mqtt_on_publish(self, mqttc, obj, mid):
		pass
		#print("Succesful publish mqtt"+ str(mid))                                 #kort nog feedback check op success
	def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
		print("Subscribed: "+str(mid)+" "+str(granted_qos))
	def mqtt_on_log(self, mqttc, obj, level, string):
		print(string)
	def run(self):
		try:
			self._mqttc.username_pw_set(ACCESS_TOKEN)
			self._mqttc.connect_async(THINGSBOARD_HOST,1883,60)
			#add later for comms back
			rc = 0
			self._mqttc.loop_start() #maybe loop_forever?
			print("Connecting to broker")
		except:
			print("Error connecting to broker")

	def publish(self,data):
		if self.Connected:
			self._mqttc.publish('v1/devices/me/telemetry', data,qos = 0)
			#print(data)

	def close(self):
		self._mqttc.loop_stop()

	
# If you want to use a specific client id, use
# mqttc = MyMQTTClass("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
if __name__ == "__main__":
	mqttc = MyMQTTClass()
	rc = mqttc.run()
	print("rc: "+str(rc))
	x = 0
	while x != 1:
		time.sleep(1)
		#mqttc.publish("sdkljbvhf")
	
