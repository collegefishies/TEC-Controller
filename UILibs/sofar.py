import ui
from liveplot import graph
from scroll_wheel import h_wheel, v_wheel
from scene import SceneView
v = ui.load_view()
v['bg'].image = ui.Image.named('background.jpg')
v['graph1'].scene = graph()
v.present('sheet')
