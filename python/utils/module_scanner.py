import importlib

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

from utils.handlers import Controller, RequestMapping
from utils import logger

def generate_handlers(module_list):

    def loop_over_modules(module_list):

        handlers = []

        for module_name in module_list:

            for controller in scan_controller_module(
                    "controllers." + module_name):

                logger.log("['{}'] Mapped to {}".format(
                        controller.url, controller.__name__))

                handlers.append((controller.url, controller))
        return handlers

    def scan_controller_module(module_name):
        module = importlib.import_module(module_name)
        module_dict = module.__dict__
        module_classes = extract_classes(module_dict)
        logger.debug(module_classes)

        controllers = []
        for klass in module_classes:
            logger.debug("Checking {}".format(klass.__name__))
            try:
                if RequestMapping in klass.decorators:
                    logger.debug("{} Found.".format(klass.__name__))
                    controllers.append(klass)
            except AttributeError:
                logger.debug("AttributeError")

        return controllers

    def extract_classes(module_dict):
        return [module_dict[key] for key in module_dict
                if (isinstance(module_dict[key], type))]

    return loop_over_modules(module_list)
