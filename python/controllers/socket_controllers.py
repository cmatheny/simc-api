from services.simc import SimcService
from utils import logger
from utils.handlers import RequestMapping, SocketController


@RequestMapping("/simulate")
class SimcSocket(SocketController):

    def __init__(self, *args):
        super().__init__(*args)
        self.return_methods = [
                "error",
                "message",
                "output",
                "result",
                "status",
                ]
        self.jobs = []
        self.service = SimcService()

    def open(self):
        logger.log("WebSocket opened")

    def on_close(self):
        logger.log("WebSocket closed")

    def simulate(self, request_json):
        pid = self.service.simc_armory_to_json(request_json,
                                               self.write_message)
        self.jobs.append(pid)
        logger.log(self.jobs)

    def cancel(self, request_json):
        logger.log(self.jobs)
        job_id = request_json["job_id"]
        if job_id not in self.jobs:
            self.write_error("Job not found")
        else:
            del self.jobs[self.jobs.index(job_id)]
        logger.log(self.jobs)
        self.service.cancel_simulation(job_id)
