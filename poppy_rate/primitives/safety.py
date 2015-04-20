from datetime import datetime, timedelta
from pypot.primitive import LoopPrimitive
import subprocess
import pypot

class CustomTemperatureMonitor(LoopPrimitive):
    '''
        This primitive raises an alert by playing a sound when the temperature
        of one motor reaches the "temp_limit".
        
        If a motor reaches the limit since more than "time_reduce_torque" seconds
        the torc of this motor will be reduced to "small_torque".
        
        If a motor reaches the limit since more than "time_compliant" seconds
        this motor will be made compliant.

        On MacOS "Darwin" you can use "afplay" for player
        On windows vista+, you can maybe use "start wmplayer"
        '''
    def __init__(self, robot, freq=0.5, temp_limit=40, 
                 time_reduce_torque=5, small_torque=20, 
                 time_compliant=10, player='aplay', sound=None):
        
        LoopPrimitive.__init__(self, robot, freq)

        self.temp_limit = temp_limit
        self.time_reduce_torque = time_reduce_torque
        self.time_compliant = time_compliant
        self.small_torque = small_torque
        self.player = player
        self.sound = sound
        self._overheat_time = {}

    def setup(self):
        pass

    def update(self):
        self.check_temperature()

    def teardown(self):
        pass

    def check_temperature(self):
        motor_list = []

        for m in self.robot.motors:
            if m.present_temperature > self.temp_limit:
                motor_list.append(m)
                if m not in self._overheat_time:
                    self._overheat_time[m] = datetime.now()
            else:
                if m in self._overheat_time:
                    del(self._overheat_time[m])

        if len(motor_list) > 0:
            self.raise_problem(motor_list)
        
        for m,t in self._overheat_time.items():
            if (datetime.now() - t) > timedelta(seconds = self.time_compliant):
                print('/!\ Making {} compliant !'.format(m.name))
                m.compliant = True

            elif(datetime.now() - t) > timedelta(seconds = self.time_reduce_torque):
                print('/!\ Reducing torque of {} to {}'.format(m.name,min(m.torque_limit,self.small_torque)))
                m.torque_limit = min(m.torque_limit,self.small_torque)

    def raise_problem(self, motor_list):
        subprocess.call([self.player, self.sound])

        for m in motor_list:
            print('{} overheating: {}'.format(m.name, m.present_temperature))

            
class TemperatureLogger(LoopPrimitive):
    def __init__(self, robot, freq=5):
        LoopPrimitive.__init__(self, robot, freq)

    # This code will be called each time the primitive is started
    def setup(self):
        self.temp_min = []
        self.temp_max = []
       
    # This method will be called at the predefined frequency
    def update(self):
        self.temp_min.append(min([m.present_temperature for m in self.robot.motors]))
        self.temp_max.append(max([m.present_temperature for m in self.robot.motors]))