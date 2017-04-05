import importlib
import utils.logger
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler


def generate_handlers(module_list):

    def loop_over_modules(module_list):
        handlers = []
        for module_name in module_list:
            for controller in scan_controller_module("controllers."
                                                     + module_name):
                utils.logger.log("[", controller.url, "] Mapped to ",
                                 controller.__name__)
                handlers.append((controller.url, controller))
        return handlers

    def scan_controller_module(module_name):
        module = importlib.import_module(module_name)
        module_dict = module.__dict__
        module_classes = extract_classes(module_dict)
        utils.logger.log([
                klass for klass in module_classes
                if issubclass(klass, RequestHandler)
                or issubclass(klass, WebSocketHandler)
                if klass is not WebSocketHandler
        ])
        return [
                klass for klass in module_classes
                if (issubclass(klass, RequestHandler))
                or issubclass(klass, WebSocketHandler)
                if klass is not WebSocketHandler
        ]

    def extract_classes(module_dict):
        return [module_dict[key] for key in module_dict
                if (isinstance(module_dict[key], type))]

    return loop_over_modules(module_list)
