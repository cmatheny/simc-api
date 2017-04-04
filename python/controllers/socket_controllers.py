import json
import utils.logger
from services.simc import SimcService as SimcService
from utils.handlers import RequestMapping, SocketController
from tornado.websocket import WebSocketHandler

@RequestMapping("/echo")
@SocketController
class EchoWebSocket(WebSocketHandler):
    
    def open(self):
        utils.logger.log("WebSocket opened")

    def on_message(self, message):
        utils.logger.log("Message received: ", message)
        self.write_message(u"You said: " + message)

    def on_close(self):
        utils.logger.log("WebSocket closed")
        
@RequestMapping("/sim")
@SocketController
class SimcWebSocket(WebSocketHandler):
    
    def open(self):
        utils.logger.log("WebSocket opened")

    def on_message(self, message):
        try:
            sim_json = json.loads(message)
        except json.decoder.JSONDecodeError:
            self.write_message("Invalid Format: Requires JSON")
        SimcService.simc_armory_to_json(sim_json)
        self.write_message(u"You said: " + message)

    def on_close(self):
        utils.logger.log("WebSocket closed")
        
