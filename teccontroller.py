import ui
import time
from controller import *
from UILibs.liveplot import *
from io import BytesIO
import matplotlib.pyplot as plt
from numpy import linspace,sin
import objc_util
import csv
import console


#change button title label behavior to allow two lines
NSLineBreakByWordWrapping = 0
NSLineBreakByCharWrapping = 1
NSLineBreakByClipping = 2
NSLineBreakByTruncatingHead = 3
NSLineBreakByTruncatingTail = 4
NSLineBreakByTruncatingMiddle = 5

def disconnect(sender):
	'@type sender: ui.Button'
	global pid, times, r, d
	if pid.connected:
		cb.cancel_peripheral_connection(pid.peripheral)
		sender.superview.close()
		exit()
def button_tapped(sender):
	'@type sender: ui.Button'
	
	global pid
	# Get the button's title for the following logic:
	t = sender.title
	
	# Get the labels:
	label = sender.superview['label1']
	label2 = sender.superview['label2']
	sound.play_effect('ui:click5')
	if t in '0123456789':
		if label.text == '0':
			# Replace 0 or last result with number:
			label.text = t
		else:
			# Append number:
			label.text += t
	elif t == 'DEL':
		textlist = list(label.text)
		if len(textlist) > 1 and not textlist[0] == '-':
			textlist.pop()
		elif len(textlist) > 2 and textlist[0] == '-':
			textlist.pop()
		else:
			textlist = ['']
		label.text = ''.join(textlist)
	elif t == '+/-':
		textlist = list(label.text)
		if len(textlist) > 0 and textlist[0] == '-':
			textlist = textlist[1:]
		else:
			if not textlist == ['0']:
				textlist = ['-'] + textlist
		label.text = ''.join(textlist)
	elif t == '.':
		if '.' not in label.text:
			label.text += '.'
	elif t == 'CLR':
		label.text = ''
	elif t == 'Set K\n(A/kΩ)':
	
		try:	
			value = float(label.text)
			pid.setK(value)
			i = label.text.find('.')
			if not i == -1:
				label.text = label.text[:i+3]
			sender.superview['Kvalue'].text = label.text
		except:
			print("Couldn’t set K")
			
		label.text = ''
	elif t == 'Set T (s)':
		try:
			value = float(label.text)
			if value:
				pid.setT(value)
				i = label.text.find('.')
				if not i == -1:
					label.text = label.text[:i+3]
				sender.superview['TiValue'].text = label.text
		except:
			print("Couldn’t set T")
		label.text = ''
	elif t == 'Set Setpoint (Ω)':
		try:
			value = float(label.text)		
			pid.setSetpoint(value)
			i = label.text.find('.')
			if not i == -1:
				label.text = label.text[:i+3]
			sender.superview['setpointValue'].text = label.text
		except:
			print("Couldn’t set setpoint")
		label.text = ''
	elif t == '':
		cb.cancel_peripheral_connection(pid.peripheral)
	elif t == 'Reset':
		pid.resetIntegration()
	elif t == 'Log':
		tt = ['Time (s)'] + times
		rr = ['Resistance (Ohms)'] + r 
		dd = ['Drive (0-1023)'] + d
		zipped = zip(tt,rr,dd)
			
			
			
		timestr = time.strftime("%Y%m%d-%H_%M_%S")
		fname = 'tecdata'+ timestr + '.dat'
		with open(fname, 'w') as f:
			writer = csv.writer(f, delimiter='\t')
			writer.writerows(zipped)
			

	
pid = PIDController()
print('Scanning for peripherals...')
cb.set_central_delegate(pid)
cb.scan_for_peripherals()
cb.set_verbose(False)

while not pid.connected:
	pass
	
console.set_idle_timer_disabled(True)
	
v = ui.load_view()

#define labels
v['label1'].alignment = ui.ALIGN_RIGHT
objc_util.ObjCInstance(v['setK']).button().titleLabel().setLineBreakMode(NSLineBreakByWordWrapping
)
v['setK'].title = 'Set K\n(A/kΩ)'

print('Waiting for K.value')
while pid.K.value is None:
	pass
print('Waiting for T.value')
while pid.T is None or pid.T.value is None:
	pass
print('Waiting for setpoint.value')
while pid.setpoint.value is None:
	pass
print('Waiting for thermistor.value')
while pid.thermistor.value is None:
	pass
print('Connected!')

v['Kvalue'].text = str(struct.unpack('<l',pid.K.value)[0]/100.)
v['setpointValue'].text = str(struct.unpack('<l',pid.setpoint.value)[0])
v['TiValue'].text = str(struct.unpack('<l',pid.T.value)[0]/100)

#objc_util.ObjCInstance(v['setK']).button().contentHorizontalAlignment = 0
buttons = list('0123456789.') + ['+/-']

for i in buttons:
	buttonname = 'button{}'.format(i)
	v[buttonname].title = '{}'.format(i)
	v[buttonname].font = ('<system>',24)
	
v['button2'].font = ('<system>',24)

#define graph
v['graphThermistor'].scene = graph()
v['graphDrive'].scene = graph()


#draw UI
v.present('full_screen', hide_title_bar=False,
orientations=['portrait'])
v['graphDrive'].scene.setLimits(xlims=(0,500),ylims=(0,1024))
v['graphThermistor'].scene.setLimits(xlims=(0,500))
v['graphDrive'].scene.setStroke(b=255)

v['thermistorValue'].text = str(
			int(
					struct.unpack('<l', pid.thermistor.value)[0]
				)
		)
		
times = []
r = []
d = []
starttime = time.time()
while pid.connected:
	v['thermistorValue'].text = str(
			int(
					struct.unpack('<l', pid.thermistor.value)[0]
				)
		)
	time.sleep(0.5)
	tt = time.time() - starttime
	rr = struct.unpack('<l', pid.thermistor.value)[0]
	dd = struct.unpack('<l', pid.drive.value)[0]
	
	times.append(tt)
	r.append(rr)
	d.append(dd)
	print('Drive: {}'.format(dd))
	v['graphThermistor'].scene.copydata(times,r)
	v['graphDrive'].scene.copydata(times,d)
print('Disconnected! Done!')
