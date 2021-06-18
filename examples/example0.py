from rockafly_grbl import RockaflyGrbl
import time

param = {
        'port'          : '/dev/ttyACM0',
        'baudrate'      : 115200,
        'step_per_rev'  : 800, 
        'deg_per_mm'    : 1.0,
        }

dev = RockaflyGrbl(param)
dev.set_max_speed(60.0)

#print('max_speed: {}'.format(dev.max_speed))
#
#print('pos: {}'.format(dev.position))
#
#dev.move_to(20, 100)
#print('pos: {}'.format(dev.position))
#
#dev.move_to(0, 100)
#print('pos: {}'.format(dev.position))
#
dev.sinusoid(20, 4.0, 1)
print('pos: {}'.format(dev.position))





