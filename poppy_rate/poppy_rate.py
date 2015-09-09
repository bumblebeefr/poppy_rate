import logging
import os
from subprocess import Popen
import sys
from threading import Thread

from .primitives.behaviour import SayHello, PlaySound, SimpleDance
logger = logging.getLogger(__name__)
SERVICE_THREADS = {}

import poppy.creatures
from poppy.creatures import AbstractPoppyCreature
from poppy.creatures.abstractcreature import camelcase_to_underscore
from poppy_humanoid.primitives.dance import SimpleBodyBeatMotion


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


class PoppyRate(AbstractPoppyCreature):

    def __new__(cls, base_path=None, config=None,
                simulator=None, scene=None, host='127.0.0.1', port=19997, id=0,
                use_snap=False, snap_host='0.0.0.0', snap_port=6969,
                use_http=False, http_host='0.0.0.0', http_port=8080,
                use_remote=False, remote_host='0.0.0.0', remote_port=4242,
                sync=True, start_services=False):

        print("new Poppyrate")
        if(simulator is None):
            creature = 'poppy_rate'
            base_path = (os.path.dirname(__import__(creature).__file__) if base_path is None else base_path)

            if config is None:
                config = os.path.join(os.path.join(base_path, 'configuration'), '{}.json'.format(creature))

        robot = poppy.creatures.PoppyHumanoid(base_path=base_path, config=config,
                                              simulator=simulator, scene=scene, host=host, port=port, id=id,
                                              use_snap=use_snap, snap_host=snap_host, snap_port=snap_port,
                                              use_http=use_http, http_host=http_host, http_port=http_port,
                                              use_remote=use_remote, remote_host=remote_host, remote_port=remote_port,
                                              sync=sync)

        cls.hookAndPegLeg(robot)
        return robot

    @classmethod
    def hookAndPegLeg(cls, robot, launch_services=False):
        '''
            Customize Poppyrate PoppyHumanoid instance, add custom pritives and whatever we need.
        '''
        logger.info("Add hook and peg leg ! ")

        robot.attach_primitive(SayHello(robot), 'say_hello')
        robot.attach_primitive(PlaySound(robot), 'play_sound')
        robot.temperature_monitoring.methods = ['start']
        robot.dance_beat_motion.properties = ['bpm', 'amplitude']
