import os

from services.application import Application
from utils import logger


if __name__ == '__main__':
    logger.debug("Debug Test")
    logger.log("Log Test")
    logger.warn("Warn Test")
    logger.err("Error Test")

    with open(os.path. expanduser("~") + "/.simc_apikey", "w") as f:
        f.write(os.environ['APIKEY'])

    app = Application()
    app.start()
