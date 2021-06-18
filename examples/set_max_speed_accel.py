from __future__ import print_function
from rockafly_grbl import RockaflyGrbl
import time

param = {
        'port'          : '/dev/ttyUSB0',
        'baudrate'      : 115200,
        'step_per_rev'  : 4000, 
        }

dev = RockaflyGrbl(param)
dev.set_max_speed(5000.0)
dev.set_max_accel(5000.0)
print('max_speed: ', dev.max_speed)
print('max_accel: ', dev.max_accel)




