from threading import Thread
from pypot.vrep import from_vrep
from poppy.creatures import PoppyHumanoid
from pypot.server import HTTPRobotServer
from pypot.server.server import RemoteRobotServer
from poppy_rate import hookAndPegLeg
import time
import logging

HTTP_HOST = '127.0.0.1'
HTTP_PORT = 8081

RPC_HOST = '127.0.0.1'
RPC_PORT = 4242

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='\033[1;30m%(asctime)s \033[0;33m%(levelname)s \033[1;32m%(threadName)s \033[0m%(module)s:%(lineno)-4s \033[0m%(message)s\033[0m')

    # initialize poppy
    logging.info("Instantiate Robot")
    robot = PoppyHumanoid(simulator='vrep')

    # ad poppyrate customizations
    logging.info("Add hook and peg leg")
    hookAndPegLeg(robot)

    # start rest web server on a background thread
    logging.info("Start HTTPRobotServer on http://{}:{}".format(HTTP_HOST, HTTP_PORT))
    wserver = HTTPRobotServer(robot, HTTP_HOST, HTTP_PORT)
    wserver_thread = Thread(target=wserver.run, name="HTTPRobotServer")
    wserver_thread.daemon = True
    wserver_thread.start()

    # start RPC server
    rserver = RemoteRobotServer(robot, RPC_HOST, RPC_PORT)
    logging.info("Start RemoteRobotServer on //{}:{}".format(RPC_HOST, RPC_PORT))
    rserver_thread = Thread(target=rserver.run, name="RemoteRobotServer")
    rserver_thread.daemon = True
    rserver_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Byebye !")
