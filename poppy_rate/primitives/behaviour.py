import logging
import os
from poppy_humanoid import PoppyHumanoid
from poppy_humanoid.primitives.dance import SimpleBodyBeatMotion
from pypot.primitive import Primitive
from subprocess import Popen
import subprocess
from types import MethodType
import random


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


def _soundplayer(directory, sound):
    def player(self):
        self._sound = os.path.join(directory, "%s.ogg" % sound)
        self.start()
        #print(['ogg123', os.path.join(directory, sound)])
        #ogg123 = Popen(['ogg123', os.path.join(directory, "%s.ogg" % sound)])
        # ogg123.wait()
    return player


class PlaySound(Primitive):

    def __init__(self, *args, **kwargs):
        logging.info(self)
        Primitive.__init__(self, *args, **kwargs)
        self.directory = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], 'media', 'sounds')
        self.properties = []
        self._sound = None
        self.update_sound_list()

    def update_sound_list(self):
        try:
            self.sounds = sorted([f[:-4] for f in os.listdir(self.directory) if f.endswith('.ogg')])
        except:
            self.sounds = []
        self.methods = ['start', 'stop', 'update_sound_list'] + ['play_{}'.format(sound) for sound in self.sounds]
        for sound in self.sounds:
            setattr(self, 'play_{}'.format(sound), MethodType(_soundplayer(self.directory, sound), self, type(self)))

    def run(self):
        if(self._sound):
            ogg123 = Popen(['ogg123', self._sound])
            self._sound = None
            ogg123.wait()
        elif self.sounds:
            Popen(['ogg123', os.path.join(self.directory, "%s.ogg" % random.choice(self.sounds))]).wait()


class SimpleDance(SimpleBodyBeatMotion):

    def __init__(self, *args, **kwargs):
        SimpleBodyBeatMotion.__init__(self, *args, **kwargs)
        self.properties = ['bpm', 'amplitude']
