import ui
import sound
from time import sleep
from taptic import taptic_peek, taptic_pop
from numpy import abs

def button_tapped(sender):
	taptic_peek()

class v_wheel(ui.View):
	def __init__(self):
		self.initialPos = None
		self.counter = 0
		
	def draw(self):
		img = ui.Image.named('vrt_wheel.jpg')
		img.draw(0,0,self.width,self.height)
	
	def touch_began(self, touch):
		self.initialPos = touch.location
		#taptic_peek()
		
	def touch_moved(self, touch):
		#print(touch.location[0])
		sound.load_effect('ui:click3')
		
		dx = -(self.initialPos[1] - touch.location[1]) 
		Dt = 100
		dt = 10
		if abs(dx) > 20:
			taptic_peek()
			sound.play_effect('ui:click4')
			
			self.initialPos = touch.location
			if dx > 0:
				self.counter += 1
			else:
				self.counter -= 1
			#taptic_peek()

class h_wheel(ui.View):
	def __init__(self):
		self.initialPos = None
		self.counter = 0
		
	def draw(self):
		img = ui.Image.named('hrz_wheel.jpg')
		img.draw(0,0,self.width,self.height)
	
	def touch_began(self, touch):
		self.initialPos = touch.location
		#taptic_peek()
		
	def touch_moved(self, touch):
		#print(touch.location[0])
		sound.load_effect('ui:click3')
		
		dx = -(self.initialPos[0] - touch.location[0]) 
		Dt = 100
		dt = 10
		if abs(dx) > 30:
			taptic_peek()
		
			sound.play_effect('ui:click4')
			
			self.initialPos = touch.location
			if dx > 0: 
				self.counter += 1
			else:
				self.counter -= 1
			#taptic_peek()
			
if __name__ == "__main__":
	v = ui.load_view()
	v.present()
	
