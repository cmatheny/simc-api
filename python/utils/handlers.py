import utils.logger
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

class RequestMapping:
    
    def __init__(self, url="/"):
        self.url = r"" + url
    
    def __call__(self, controller):
        controller.url = self.url
        
        return controller

class Controller:
    def __init__(self, *args):
        utils.logger.debug(args)
        self.controller = args[-1]
        
class SocketController(Controller):
    def __init__(self, *args):
        super().__init__(*args)
    
    def __call__(self, controller):
        socket_controller = type(controller.__name__, (controller,
                WebSocketHandler), {})
        
        return socket_controller
    
class RestController(Controller):
    def __init__(self, *args):
        utils.logger.debug(args)
    
    def __call__(self, controller):
        request_controller = type(controller.__name__, (controller,
                RequestHandler), {})
        
        def check_origin(self, origin):
            return True
        
        request_controller.check_origin = check_origin
        utils.logger.debug(dir(request_controller))
        return request_controller
    
