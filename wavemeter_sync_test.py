from wlm import *

wlm = WavelengthMeter()

a = wlm.switcher_mode 

print(a)

b = wlm.set_switcher_mode(1)

print(b)

a = wlm.switcher_mode 

print(a)
