import json
import traceback

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

    def check_origin(self, origin):
        return True


class SocketController(Controller, WebSocketHandler):
    def __init__(self, *args, idle_timeout=3600):
        super().__init__(*args)

    def on_message(self, message):
        logger.log("'{}' recieved from client".format(message))

        try:
            message_json = json.loads(message)
        except json.decoder.JSONDecodeError:
            self.write_message("Invalid Format", "error")
            return

        method_name = message_json[0]
        data_json = message_json[1]

        try:
            method = getattr(self, method_name)
        except AttributeError:
            self.write_message("Invalid Method.", "error")
            return

        try:
            method(data_json)
        except TypeError:
            self.write_message("Server Error", "error")
            traceback.print_exc()

    def write_message(self, data, method="message"):
        response = json.dumps([method, data])
        super().write_message(response)


class RestController(Controller, RequestHandler):
    def __init__(self, *args):
        super().__init__(*args)
