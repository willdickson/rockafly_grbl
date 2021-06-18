from __future__ import print_function
from grbl_comm import GrblComm
import math

MIN_PER_SEC = 1/60.0
SEC_PER_MIN = 60.0

class RockaflyGrbl(object):

    CIRCLE_DIR_TO_SIGN = {
            'pos':  1,
            'neg': -1,
            }

    def __init__(self, param):
        self.param = param
        self.comm = GrblComm(port=self.param['port'], baudrate=self.param['baudrate'])
        self.update_settings()
        self.check_settings()
        #for k,v in self.settings.items():
        #    print(k,v)

    def update_settings(self):
        self.settings = self.comm.get_settings()

    def check_settings(self):
        x_step_per_mm = self.settings['x_step_per_mm']
        y_step_per_mm = self.settings['y_step_per_mm']
        if x_step_per_mm != y_step_per_mm:
            raise RuntimeError('x_step_per_mm must equal y_step_per_mm')
        x_max_rate_mm_per_min = self.settings['x_max_rate_mm_per_min']
        y_max_rate_mm_per_min = self.settings['y_max_rate_mm_per_min']
        if x_max_rate_mm_per_min != y_max_rate_mm_per_min:
            raise RuntimeError('x_max_rate_mm_per_min must equal y_max_rate_mm_per_min')
        x_accel_mm_per_sec2 = self.settings['x_accel_mm_per_sec2']
        y_accel_mm_per_sec2 = self.settings['y_accel_mm_per_sec2']
        if x_accel_mm_per_sec2 != y_accel_mm_per_sec2:
            raise RuntimeError('x_accel_mm_per_sec2 must equal y_accel_mm_per_sec2')

    def convert_deg_to_mm(self,val):
        return val*self.mm_per_deg

    def convert_mm_to_deg(self,val):
        return val*self.deg_per_mm

    @property
    def max_speed(self):
        """ Returns max speed in deg/sec """
        max_rate_deg_per_min = self.convert_mm_to_deg(self.settings['x_max_rate_mm_per_min'])
        max_rate_deg_per_sec = max_rate_deg_per_min*MIN_PER_SEC
        return max_rate_deg_per_sec

    @property
    def max_accel(self):
        """ Returns linear move acceleration in deg/sec^2 """
        return self.convert_mm_to_deg(self.settings['x_accel_mm_per_sec2'])
        
    @property
    def step_per_rev(self):
        return self.param['step_per_rev']

    @property
    def step_per_deg(self):
        return self.step_per_rev/360.0

    @property
    def deg_per_step(self):
        return 360.0/self.step_per_rev

    @property
    def deg_per_mm(self):
        return self.deg_per_step*self.step_per_mm

    @property
    def mm_per_deg(self):
        return self.step_per_deg/self.step_per_mm

    @property
    def step_per_mm(self):
        return self.settings['x_step_per_mm']

    @property
    def mm_per_step(self):
        return 1.0/self.step_per_mm

    @property
    def status(self):
        return self.comm.get_status()

    @property
    def mode(self):
        return self.status['mode']

    @property
    def position(self):
        """ Returns the current position in deg """
        return self.convert_mm_to_deg(self.x_position_mm)

    @property
    def x_position_mm(self):
        return self.status['WPos']['x']

    @property
    def y_position_mm(self):
        return self.status['WPos']['y']

    @property
    def xy_position_mm(self):
        status = self.status
        return status['WPos']['x'], status['WPos']['y']

    def set_step_per_mm(self, step_per_mm):
        """ Set the number of steps per mm """
        self.comm.set_x_step_per_mm(step_per_mm)
        self.comm.set_y_step_per_mm(step_per_mm)
        self.comm.set_y_step_per_mm(step_per_mm)
        self.update_settings()

    def set_max_speed(self,speed):
        """ Set the max_speed (deg/sec) """
        speed_mm_per_min = self.convert_deg_to_mm(speed)*SEC_PER_MIN
        self.comm.set_x_max_rate_mm_per_min(speed_mm_per_min)
        self.comm.set_y_max_rate_mm_per_min(speed_mm_per_min)
        self.comm.set_z_max_rate_mm_per_min(speed_mm_per_min)
        self.update_settings()

    def set_max_accel(self,accel):
        """ Set the max_accel (deg/sec**2) """
        accel_mm_per_sec2 = self.convert_deg_to_mm(accel)
        self.comm.set_x_accel_mm_per_sec2(accel_mm_per_sec2)
        self.comm.set_y_accel_mm_per_sec2(accel_mm_per_sec2)
        self.comm.set_z_accel_mm_per_sec2(accel_mm_per_sec2)
        self.update_settings()

    def move_to(self, pos, speed):
        """ Linear move to pos (deg) at speed (deg/sec) """
        if speed > self.max_speed:
            raise RuntimeError('speed is > max_speed setting')
        pos_mm = self.convert_deg_to_mm(pos)
        feedrate_mm_per_min = self.convert_deg_to_mm(speed)*SEC_PER_MIN
        gcode_cmd = 'G1 F{0:1.3f} X{1:1.3f}'.format(feedrate_mm_per_min, pos_mm)
        self.comm.send_gcode([gcode_cmd])

    def sinusoid(self, amplitude, period, cycles, direction='pos'):
        """ 
        Run sinusoid (cosine) starting from the current position 

        theta = amplitude*cos(2.0*PI*t/period)

        amplitude  = amplitude of sinusoid (deg), float
        period     = period of sinusoid (sec),    float
        cycles     = number of cycles to run,     integer
        direction  = direction of sinusoid 'pos' or 'neg'

        """
        speed = abs(amplitude*(2.0*math.pi/period))
        #print('speed: {}, max_speed: {}'.format(speed, self.max_speed))
        if speed > self.max_speed:
            raise RuntimeError('sinusoid speed > max_speed')
        accel = abs(amplitude*(2.0*math.pi/period)**2)
        #print('accel: {}, max_accel: {}'.format(accel, self.max_accel))
        if accel > self.max_accel:
            raise RuntimeError('sinusoid accel > max_accel')
        amplitude_mm = self.convert_deg_to_mm(amplitude)
        feedrate_mm_per_min = self.convert_deg_to_mm(speed)*SEC_PER_MIN 

        offset_sign= self.CIRCLE_DIR_TO_SIGN[direction]
        x_pos_mm, y_pos_mm = self.xy_position_mm

        gcode_dict = {
                'cmd' : 'G2',
                'F'   : feedrate_mm_per_min,
                'X'   : x_pos_mm, 
                'Y'   : y_pos_mm, 
                'I'   : offset_sign*(x_pos_mm + amplitude_mm),
                }
        gcode_cmd = '{cmd} F{F:1.3f} X{X:1.3f} Y{Y:1.3f} I{I:1.3f}'.format(**gcode_dict)
        gcode_list = [gcode_cmd for i in range(cycles)]
        self.comm.send_gcode(gcode_list)


