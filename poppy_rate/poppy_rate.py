from poppy_humanoid import PoppyHumanoid
from .primitives.behaviour import SayHello

from threading import Thread
from pypot.vrep import from_vrep
from pypot.server import HTTPRobotServer
from pypot.server import RemoteRobotServer


def hookAndPegLeg(robot, launch_services=False):
    '''
        Customize Poppyrate PoppyHumanoid instance, add custom pritives and whatever we need.
    '''
    robot.attach_primitive(SayHello(robot), 'say_hello')
