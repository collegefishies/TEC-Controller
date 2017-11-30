import ui, scene
from scene import SceneView
import scene_drawing as sd
import numpy as np


class simpleGraph(scene.Scene):
	def setup(self):
		#initialize memory
		self.xdata = np.empty(self.size[0])
		self.ydata = np.empty(self.size[1])
		self.xlims = (0, 10)
		self.ylims = (-1, 1)
		
		#set background
		#self.background_color = 'white'
		pass
	
	def changeXaxis(self):
		#change xlims
		pass
	
	def changeYaxis(self):
		#change ylims
		pass
		
	def rescaler(self, x, y):
		#return pixels instead of data
		xp = (x - self.xlims[0])/(self.xlims[1] - self.xlims[0])
		yp = (y - self.ylims[0])/(self.ylims[1] - self.ylims[0])
		xp = xp*self.size[0]
		yp = yp*self.size[1]
		
		return (xp, yp)
		
	def draw(self):
		#draw Axes
		sd.stroke_weight(2)
		sd.stroke(0, 0, 0)
		
		sd.line(0,0, 0, self.size[1])
		sd.line(0,0, self.size[0], 0)
		
		#draw Grid
		
		#draw Labels
		
		#draw Line
		sd.stroke_weight(1)
		sd.stroke(255, 0, 0)
		
		for i in range(len(self.xdata) - 1):
			xpi, ypi = self.rescaler( self.xdata[i], 
				self.ydata[i] )
			xpii, ypii = self.rescaler( self.xdata[i+1],
				self.ydata[i+1] )
			sd.line(xpi, ypi, xpii, ypii)
		pass

if __name__ == '__main__':
	v = ui.load_view()
	v['view1'].scene = simpleGraph()
	v.present('sheet')
	
