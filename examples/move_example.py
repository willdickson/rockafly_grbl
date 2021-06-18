from __future__ import print_function
from rockafly_grbl import RockaflyGrbl
import time

param = {
        'port'          : '/dev/ttyUSB0',
        'baudrate'      : 115200,
        'step_per_rev'  : 4000, 
        }

dev = RockaflyGrbl(param)


print('pos: {}'.format(dev.position))

dev.move_to(90, 20)

print('pos: {}'.format(dev.position))

dev.move_to(0, 20)

print('pos: {}'.format(dev.position))





