import importlib
import os

import tornado.ioloop
import tornado.web
import tornado.websocket

import ignore
import services.simc
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
    print(ignore.Test.callit(2))

    with open(os.path. expanduser("~") + "/.simc_apikey", "w") as f:
        f.write(os.environ['APIKEY'])

    logger.debug("Debug Test")
    logger.log("Log Test")
    logger.warn("Warn Test")
    logger.err("Error Test")
    app = make_app()
    service = services.simc.SimcService()
    tornado.ioloop.IOLoop.current().start()
