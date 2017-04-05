import importlib
import os

import tornado.ioloop
import tornado.web
import tornado.websocket

from services.simc import SimcService
from utils import logger
from utils import module_scanner


def make_app(settings_file="config.settings"):
    settings = importlib.import_module(settings_file)
    handlers = module_scanner.generate_handlers(settings.CONTROLLER_MODULES)
    app = tornado.web.Application(handlers)
    app.listen(settings.SERVER_PORT)
    logger.log("Server listening on port: ", settings.SERVER_PORT)
    return app

if __name__ == '__main__':
    logger.debug("Debug Test")
    logger.log("Log Test")
    logger.warn("Warn Test")
    logger.err("Error Test")

    with open(os.path. expanduser("~") + "/.simc_apikey", "w") as f:
        f.write(os.environ['APIKEY'])

    app = make_app()
    #service = SimcService()
    tornado.ioloop.IOLoop.instance().start()
    logger.log("Going down.")
    tornado.ioloop.IOLoop.instance().stop()
