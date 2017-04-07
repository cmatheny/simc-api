import json

import tornado.ioloop

from services.simc import SimcService as SimcService
from utils import logger
from utils.handlers import RequestMapping, SocketController


@RequestMapping("/echo")
class EchoWebSocket(SocketController):

    def open(self):
        logger.log("WebSocket opened")

    def on_message(self, message):
        logger.log("Message received: ", message)
        self.write_message(u"You said: " + message)

    def on_close(self):
        logger.log("WebSocket closed")


@RequestMapping("/sim")
class SimcWebSocket(SocketController):

    def open(self):
        logger.log("WebSocket opened")

    def on_message(self, message):
        try:
            sim_json = json.loads(message)
        except json.decoder.JSONDecodeError:
            self.write_message("Invalid Format: Requires JSON")
        SimcService.simc_armory_to_json(sim_json)
        self.write_message(u"You said: " + message)

    def on_close(self):
        logger.log("WebSocket closed")


@RequestMapping("/troll")
class TrollSocket(SocketController):

    def open(self):
        logger.log("WebSocket opened")
        self.counter = 0
        self.write_message("Hello, How are you?")
        self.messages = [
                "That's nice. Anything else?",
                "I don't like you.",
                "I'm leaving. Bye.",
                ]

    def on_message(self, message):
        logger.log(self.counter)
        if self.counter is 0:
            self.write_message(self.messages[0])
        else:
            self.write_message(self.messages[self.counter])
        logger.log(self.counter)
        self.counter += 1
        if self.counter is 3:
            self.close()

    def on_close(self):
        logger.log("WebSocket closed")

    def do_troll(self):
        pass


@RequestMapping("/async")
class AsyncSocket(SocketController):

    def __init__(self, *args):
        super().__init__(*args)
        self.return_methods = [
                "message"
                "result"
                ]
        self.service = SimcService()

    def open(self):
        logger.log("WebSocket opened")

    def on_close(self):
        logger.log("WebSocket closed")

    def simulate(self, request_json):
        self.service.simc_armory_to_json(request_json, self.write_message)
