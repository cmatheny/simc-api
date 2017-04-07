from importlib import import_module

import tornado.ioloop
import tornado.web

from utils import module_scanner, logger
from utils.misc import singleton


@singleton
class Application(tornado.web.Application):

    def __init__(self, *args, settings_file="config.settings"):
        self.config = import_module(settings_file)
        self.handlers = module_scanner.generate_handlers(
                self.config.CONTROLLER_MODULES)
        logger.log(self.handlers)
        super().__init__(*args, handlers=self.handlers)
        self.listen(self.config.SERVER_PORT)
        logger.log("Server listening on port: ", self.config.SERVER_PORT)

    def start(self):
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        logger.log("Going down.")
        tornado.ioloop.IOLoop.instance().stop()
