import matplotlib.pyplot as plt
from numpy import linspace, sin, diff
import numpy as np
import scene_drawing as sd
from scene import *
import ui
import time
import motion
from random import random

### need set xlims, set ylims
### need set stroke color!!!

class graph(Scene):
	def setup(self):
		self.background_color=(0,0,0,0)
		self.xdata = np.zeros(self.size[0], float)
		self.ydata = np.zeros(self.size[0], float)
		self.xtemp = np.zeros(self.size[0], float)
		self.ytemp = np.zeros(self.size[0], float)
		self.xlims = (0,30)
		self.ylims = (8e3,18e3)
		self.r = 0
		self.g = 255
		self.b = 0
	def setLimits(self, xlims=None, ylims=None):
		if xlims is not None:
			self.xlims = xlims
		if ylims is not None:
			self.ylims = ylims
	
	def setStroke(self, r = 0, g =0, b =0):
		self.r = r
		self.g = g
		self.b = b
		
	def draw(self):
		sd.stroke_weight(1)
		sd.stroke(self.r,self.g,self.b)
		
		self.xdata = np.copy(self.xtemp)
		self.ydata = np.copy(self.ytemp)

		self.plot(self.xdata, self.ydata)
		
	def draw_test(self):
		sd.stroke_weight(1)
		sd.stroke(0,255,0)
		
		timenow = time.time()
		x = linspace(-30,0,self.size[0])
		y = 100*sin((x-timenow)) + 10e3
		
		#renormalize data
		x,y = self.resize(x,y)

		self.plot(x,y)
				
	def resize(self,x,y):
		x = np.array(x)
		y = np.array(y)
		y = (y - self.ylims[0])/diff(self.ylims)*self.size[1]
		x = (x - self.xlims[0])/diff(self.xlims)*self.size[0]
		return (x,y)
	def resize_single(self, x, y):
		y = (y - self.ylims[0])/diff(self.ylims)*self.size[1]
		x = (-x + self.xlims[1])/diff(self.xlims)*self.size[0]
		return (x,y)
	
	def plot(self,x,y):
		for i in range(len(x) - 1):
			sd.line(x[i],y[i],x[i+1],y[i+1])
	
	def copydata(self, u,v):
		for i in range(len(self.xdata)):
			try:
				x,y = self.resize_single(u[-1] - u[-1-i], v[-1-i])		
				self.xtemp[i] = x
				self.ytemp[i] = y
			except:
				break
				
if __name__ == '__main__':
	v = ui.load_view()
	v['view1'].scene = graph()
	v['view1'].anti_alias = True
	v.present('panel')
	
	t = []
	r = []
	starttime = time.time()
	while True:
		time.sleep(0.1)
		a = 1000*random() + 10e3
		tt = time.time() - starttime
		t.append(tt)
		r.append(a)
		v['view1'].scene.copydata(t,r)
