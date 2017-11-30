import cb
import sound
import time
import struct
from random import random


class PIDController (object):
	def __init__(self):
		self.peripheral = None
		self.K = None
		self.T = None
		self.drive = None
		self.driveValue = None
		self.setpoint = None
		self.thermistor = None
		self.reset = None
		self.connected = False
		

	def did_discover_peripheral(self, p):
		if not self.connected:
			print("Found: {}".format(p.name))
		if p.name and 'Fermi.2: DMD TEC' in p.name and not self.peripheral:
			self.peripheral = p
			print('Connecting to DMD TEC Controller...')
			time.sleep(2)
			cb.connect_peripheral(p)

	def did_connect_peripheral(self, p):
		print('Connected: ', p.name)
		print('Discovering services...')
		p.discover_services()

	def did_fail_to_connect_peripheral(self, p, error):
		print('Failed to connect: {}'.format(error))

	def did_disconnect_peripheral(self, p, error):
		print('Disconnected, error: {}'.format(error))
		self.peripheral = None
		self.connected = False
		print('Scanning for peripherals')

	def did_discover_services(self, p, error):
		for s in p.services:
			if s.uuid == '1815':
				print('Discovered Automation IO service, discovering characteristics...')
				p.discover_characteristics(s)
		print('Finished discovering services...')

	def did_discover_characteristics(self, s, error):
		print('Did discover characteristics...')
		for c in s.characteristics:
			if c.uuid == '2A7E':
				print('+++ K')
				self.K = c
				self.peripheral.read_characteristic_value(c)
			if c.uuid == '2A7F':
				self.T = c
				self.peripheral.read_characteristic_value(c)
				print('+++ T')
			if c.uuid == '2A80':
				self.drive = c
				self.peripheral.set_notify_value(c,True)
				print('+++ Drive')
				self.connected = True
			if c.uuid == '1B7F':
				self.setpoint = c
				self.peripheral.read_characteristic_value(c)
				print('+++ Setpoint')
			if c.uuid == '2B7F':
				self.thermistor = c
				self.peripheral.set_notify_value(c,True)
				print('+++ Thermistor')
			if c.uuid == '2B80':
				self.reset = c
				print('+++ Reset')
				
			#prop = c.properties
			#print("Properties: ")
			#print("		Write? {}".format(prop & cb.CH_PROP_WRITE))
			#print("		Write w/o response? {}".format(prop & cb.CH_PROP_WRITE_WITHOUT_RESPONSE))				
			
	def did_update_value(self, c, error):
		if c.uuid == '2A80':
			unpackedDrive = struct.unpack('<i',self.drive.value)[0]
			self.driveValue = unpackedDrive
			pass
	
	def did_write_value(self, c, error):
		pass
	def setK(self,newK):
		if self.K is None:
			print("Error: No K Characteristic")
			return
		if self.peripheral is None:
			return
		packedK = struct.pack('<l', int(newK*100))
		print("Setting 100K to :  {}".format(int(newK*100)))
		self.peripheral.write_characteristic_value(self.K, packedK, True)
		time.sleep(0.2)
		pass
	
	def setT(self,newK):
		if self.T is None:
			print("Error: No T characteristic")
			return
		if self.peripheral is None:
			return
		packedK = struct.pack('<l', int(newK*100))
		self.peripheral.write_characteristic_value(self.T, packedK, True)
		print("Setting 100T to :  {}".format(int(newK*100)) )
		time.sleep(0.2)
		pass
	
	def setSetpoint(self,newK):
		if self.setpoint is None:
			print("Error: No setpoint characteristic")
			return
		if self.peripheral is None:
			return
		packedK = struct.pack('<l', int(newK))
		print("Setting Setpoint to : {}".format(int(newK)))
		self.peripheral.write_characteristic_value(self.setpoint, packedK, True)
		time.sleep(0.2)
		pass
	
	def resetIntegration(self):
		if self.reset is None:
			print("Error: No reset characteristic.")
		if self.peripheral is None:
			return
		packedR = struct.pack('<l',int(1))
		print("Resetting Integration")
		self.peripheral.write_characteristic_value(self.reset, packedR, True)
	
	def __del__(self):
		if not self.peripheral is None:
			cb.cancel_peripheral_connection(self.peripheral)
			
			


if __name__ == '__main__':

	pid = PIDController()
	print('Scanning for peripherals...')
	cb.set_central_delegate(pid)
	cb.scan_for_peripherals()
	cb.set_verbose(False)
	
	try:
		time.sleep(10)
		while True:
			try:
				setpoint = struct.unpack('<l', pid.setpoint.value)[0]
				print("setpoint read to be: {}".format(setpoint))
			except:
				pass
			
			pid.setSetpoint(10000*random())
			pid.setK(100*random())
			pid.setT(1000*random())
			time.sleep(0.1)
			pass
	except KeyboardInterrupt:
		cb.reset()
