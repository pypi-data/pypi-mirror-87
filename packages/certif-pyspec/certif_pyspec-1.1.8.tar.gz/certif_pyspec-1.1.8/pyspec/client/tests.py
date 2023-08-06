
from pyspec.css_logger import log
from pyspec.client import SpecConnection
#from pyspec.client.SpecConnection import SpecConnection
import pyspec.client

def test_splot():
    ldt = pyspec.client.variable(spec, 'LDT')
    print(ldt.get())
    
def test_channels():
    chan = spec.get_channel('var/MYVAR')
    print(chan.read())
    chan.write(45)
    print(chan.read())

def test_motors():
    mot = spec.get_motor('chi')
    print("Position: %s" % mot.position)
    print("Velocity: %s" % mot.read("slew_rate"))
    mot.mv(1)

def test_variables():
    pass

def test_commands():
    pass

import sys

log.start()
spec = SpecConnection(sys.argv[1])

test_splot()

#test_channels()
#test_motors()

