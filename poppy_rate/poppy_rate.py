import logging
import os
from poppy.creatures import PoppyHumanoid
from poppy.creatures.abstractcreature import camelcase_to_underscore
from poppy_humanoid.primitives.dance import SimpleBodyBeatMotion
from subprocess import Popen
import sys
from threading import Thread

from .primitives.behaviour import SayHello, PlaySound, SimpleDance
logger = logging.getLogger(__name__)
SERVICE_THREADS = {}


class DeamonThread(Thread):

    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.setDaemon(True)

    def run(self, *args, **kwargs):
        try:
            logger.info("Start thread %s" % self)
            Thread.run(self, *args, **kwargs)
        except:
            logger.exception("Error on thread %s " % self)


class PoppyRate(PoppyHumanoid):

    def __new__(cls, base_path=None, config=None,
                simulator=None, scene=None, host='127.0.0.1', port=19997, id=0,
                use_snap=False, snap_host='0.0.0.0', snap_port=6969,
                use_http=False, http_host='0.0.0.0', http_port=8080,
                use_remote=False, remote_host='0.0.0.0', remote_port=4242,
                sync=True, start_services=False):

        if(simulator is None):
            creature = 'poppy_rate'
            base_path = (os.path.dirname(__import__(creature).__file__) if base_path is None else base_path)

            if config is None:
                config = os.path.join(os.path.join(base_path, 'configuration'), '{}.json'.format(creature))

        robot = PoppyHumanoid(base_path=base_path, config=config,
                              simulator=simulator, scene=scene, host=host, port=port, id=id,
                              use_snap=use_snap, snap_host=snap_host, snap_port=snap_port,
                              sync=sync)

        if(use_http):
            from pypot.server import HTTPRobotServer
            robot.http = HTTPRobotServer(robot, http_host, http_port, cross_domain_origin="*")

        if(use_remote):
            from pypot.server import RemoteRobotServer
            robot.remote = RemoteRobotServer(robot, remote_host, remote_port)

        cls.hookAndPegLeg(robot)

        if(start_services):
            cls.start_background_services(robot)
            PoppyRate.play_sound('modem.wav', wait=False)

        return robot

    @classmethod
    def play_sound(cls, sound, wait=True):
        logger.info("Playing sound {}".format(sound))
        try:
            player = Popen(['aplay', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'sounds', sound)])
            if wait:
                player.wait()
        except:
            logger.exception("Error playing sound {}".format(sound))

    @classmethod
    def start_background_services(cls, robot, services=['snap', 'http', 'remote']):
        for service in services:
            if(hasattr(robot, service)):
                if service in SERVICE_THREADS:
                    logger.warning("A {} background service is already running, you may have to restart your script or reset your notebook kernel to start it again.".format(service))
                else:
                    SERVICE_THREADS[service] = DeamonThread(target=getattr(robot, service).run, name="{}_server".format(service))
                    SERVICE_THREADS[service].daemon = True
                    SERVICE_THREADS[service].start()
                    logger.info("Starting {} service".format(service))

    @classmethod
    def hookAndPegLeg(cls, robot, launch_services=False):
        '''
            Customize Poppyrate PoppyHumanoid instance, add custom pritives and whatever we need.
        '''
        logger.info("Add hook and peg leg ! ")

        robot.attach_primitive(SayHello(robot), 'say_hello')
        robot.attach_primitive(PlaySound(robot), 'play_sound')
        robot.attach_primitive(SimpleDance(robot, 120, motion_amplitude=20), 'dance')
        robot.temperature_monitoring.methods = ['start']
