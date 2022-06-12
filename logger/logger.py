import logging
from hashlib import md5
from datetime import datetime

TIMESTAMP = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
SIMULATION_ID = md5(TIMESTAMP.encode('utf-8')).hexdigest()

def setup_logger(level):
    try:
        level = getattr(logging, level)
        filename = f"simulation_{TIMESTAMP}_{SIMULATION_ID}.log"
        logging.basicConfig(filename=filename,
                            format='[%(asctime)s] - %(levelname)-5s (%(filename)s:%(lineno)s %(funcName)s) %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filemode='w')
        logging.getLogger().setLevel(level)
        logging.captureWarnings(True)
        return True
    except Exception as exc:
        logging.error(exc, exc_info=True)
        return False

class Logger:

    @staticmethod
    def create_logger(name):
        return logging.getLogger(name)