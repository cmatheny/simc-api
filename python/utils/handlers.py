from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

from utils import logger


def register_decorator(decorator, decorated):
    try:
        decorated.decorators.add(decorator.__class__)
    except:
        decorated.decorators = {decorator.__class__}
    logger.debug(decorated, " decorators: ", decorated.decorators)


class RequestMapping:

    def __init__(self, url="/"):
        logger.debug("Self: ", self)
        self.url = r"" + url

    def __call__(self, controller):
        logger.debug("Controller: ", controller)
        controller.url = self.url
        register_decorator(self, controller)
        return controller


class Controller():
    def __init__(self, *args):
        super().__init__(*args)
        logger.debug(self.__class__.__name__, " created")


class SocketController(Controller, WebSocketHandler):
    def __init__(self, *args):
        super().__init__(*args)


class RestController(Controller, RequestHandler):
    def __init__(self, *args):
        super().__init__(*args)

    def check_origin(controller, origin):
        return True
