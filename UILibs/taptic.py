from objc_util import * 
import ui
UIDevice = ObjCClass('UIDevice')

def taptic_peek():
    d = UIDevice.new()
    t = d._tapticEngine()
    t.actuateFeedback_(1001)   # or t.actuateFeedback_(0)
    
def taptic_pop():
    d = UIDevice.new()
    t = d._tapticEngine()
    t.actuateFeedback_(1002)   # or t.actuateFeedback_(1)

def taptic_triple_knock():
    d = UIDevice.new()
    t = d._tapticEngine()
    t.actuateFeedback_(2)
    

