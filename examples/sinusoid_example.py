from __future__ import print_function
from rockafly_grbl import RockaflyGrbl
import time

param = {
        'port'          : '/dev/ttyUSB0',
        'baudrate'      : 115200,
        'step_per_rev'  : 4000, 
        }

dev = RockaflyGrbl(param)

dev.sinusoid(720.0, 16.0, 5, direction='neg')



