from rockafly_grbl import RockaflyGrbl
import time

param = {
        'port'          : '/dev/ttyUSB0',
        'baudrate'      : 115200,
        'step_per_rev'  : 800, 
        }

dev = RockaflyGrbl(param)
dev.set_max_speed(800)
dev.set_max_accel(1000)
print('max_speed     ', dev.max_speed)
print('max_accel     ', dev.max_accel)
print('step_per_mm:  ', dev.step_per_mm)
print('mm_per_step:  ', dev.mm_per_step)
print('step_per_deg: ', dev.step_per_deg)
print('deg_per_step: ', dev.deg_per_step)
print('mm_per_deg:   ', dev.mm_per_deg)
print('deg_per_mm:   ', dev.deg_per_mm)
print(dev.convert_deg_to_mm(20))

#print('pos: {}'.format(dev.position))
#
#dev.move_to(20, 100)
#print('pos: {}'.format(dev.position))
#
#dev.move_to(0, 100)
#print('pos: {}'.format(dev.position))
#
print('running sinusoid')
dev.sinusoid(45.0, 4.0, 2)
print('pos: {}'.format(dev.position))





