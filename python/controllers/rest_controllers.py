from utils import logger
from utils.handlers import RestController, RequestMapping


@RequestMapping(url="/")
class MainController(RestController):
    def get(self):
        logger.log("Hello, world")
        self.write("HI")
