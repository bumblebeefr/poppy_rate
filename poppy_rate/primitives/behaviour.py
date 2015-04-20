from pypot.primitive import Primitive
from poppy_humanoid import PoppyHumanoid


def _mirror_position(position):
    '''
        Assume angles values are given for a right part 
        of the robot and reverse x and z angles when used 
        for left site motors.

    '''
    return dict([(k, (v, -v)[k[0] == 'l' and k[-1] in ['x', 'z']]) for k, v in position.items()])


class SayHello(Primitive):

    def run(self):
        motor_state = dict([(m.name, m.compliant) for m in self.robot.arms])
        for m in self.robot.arms:
            m.compliant = False

        for p in ['r', 'l']:
            self.robot.goto_position(_mirror_position({'%s_elbow_y' % p: -50, '%s_shoulder_y' % p: -165, '%s_arm_z' % p: 90}), 1.5, wait=True)

            for k in range(3):
                self.robot.goto_position(_mirror_position({'%s_elbow_y' % p: -30, '%s_shoulder_x' % p: -40}), 0.7, wait=True)
                self.robot.goto_position(_mirror_position({'%s_elbow_y' % p: -65, '%s_shoulder_x' % p: 0}), 0.7, wait=True)

            self.robot.goto_position(_mirror_position({'%s_elbow_y' % p: 0, '%s_shoulder_y' % p: 0, '%s_arm_z' % p: 0, '%s_shoulder_x' % p: -15}), 2, wait=True)

        for m, c in motor_state.items():
            self.robot.__dict__.get(m).compliant = c
