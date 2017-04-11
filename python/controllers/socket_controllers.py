from services.simc import SimcService
from utils import logger
from utils.handlers import RequestMapping, SocketController


@RequestMapping("/simulate")
class AsyncSocket(SocketController):

    def __init__(self, *args):
        super().__init__(*args)
        self.return_methods = [
                "error",
                "message",
                "output",
                "result",
                "status",
                ]
        self.service = SimcService()

    def open(self):
        logger.log("WebSocket opened")

    def on_close(self):
        logger.log("WebSocket closed")

    def simulate(self, request_json):
        self.service.simc_armory_to_json(request_json, self.write_message)
