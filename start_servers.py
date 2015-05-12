import logging
from threading import Thread
import logging.handlers
from poppy_rate import PoppyRate
import time
import signal
import os
import subprocess
import sys
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    handler = logging.handlers.TimedRotatingFileHandler('logs/poppyrate.log', when="midnight", backupCount=10)
    formatter = logging.Formatter('\033[1;30m%(asctime)s \033[0;33m%(levelname)s \033[1;32m%(threadName)s \033[0m%(module)s:%(lineno)-4s \033[0m%(message)s\033[0m')
    handler.setFormatter(formatter)
    handler.setLevel('INFO')
    logging.root.handlers = []
    logging.root.addHandler(handler)
    logging.root.setLevel('INFO')

    try:
        robot = PoppyRate(use_snap=True, use_remote=True, use_http=True, start_services=True, )#simulator='vrep')
    except:
        logger.exception("Unable to Start Robot Instance")

    def sigterm_handler(signum, frame):
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shuting down")
        robot.compliant = True
        subprocess.call(['aplay', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'poppy_rate', 'media', 'sounds', 'au_revoir.wav')])
    except SystemExit:
        logger.info("Shuting down")
        robot.compliant = True
        subprocess.call(['aplay', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'poppy_rate', 'media', 'sounds', 'au_revoir.wav')])
    except:
        logger.exception("Shuting down")
        robot.compliant = True
