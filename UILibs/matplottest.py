import ui
import matplotlib.pyplot as plt
import numpy as np
import time

fig,ax = plt.subplots()
line, = ax.plot(np.random.randn(100))
plt.show()
tstart = time.time()
num_plots = 0

while time.time() - tstart < 1:
	line.set_ydata(np.random.randn(100))
	ax.draw_artist(ax.patch)
	ax.draw_artist(line)
	#fig.canvas.update()
	#fig.canvas.flush_events()
	fig.canvas.draw()
	#fig.canvas.flush_events()
	num_plots += 1

print(num_plots)
	

#v = ui.load_view()
#v.present('sheet')
