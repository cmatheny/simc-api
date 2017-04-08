import math
from concurrent.futures import ThreadPoolExecutor
import random
import subprocess
import collections

import tornado.ioloop
import tornado.process
import tornado.gen

from exceptions.exceptions import ProcessFailureException
from utils import logger
from services.application import Application


def run_job(proc):
    logger.log("Starting Simulation Thread.")
    logger.log(proc)
    return subprocess.call(proc)


class ProcessManager:

    def __init__(self):
        pass
        self.jobs = {
            'queued': collections.deque(),
            'running': [],
        }
        self.app = Application()
        self.executor = ThreadPoolExecutor(max_workers=2)

    def generate_random_pid(self):
        while True:
            pid = math.floor(random.randrange(100000, 999999))
            if not (any(proc == pid for proc in self.jobs["queued"]) and
                    any(proc == pid for proc in self.jobs["running"])):
                return pid

    async def run_job(self, command, pid=None, out=logger.null):

        pid = pid if pid else self.generate_random_pid()

        if len(self.jobs["running"]) >= self.app.config.MAX_SIM_THREADS:
            self.jobs["queued"].append(pid)
            logger.log(self.jobs)
            out("Job #{} Queued at position {}.".format(
                    pid, len(self.jobs["queued"])))
            while self.jobs["queued"][0] is not pid or len(
                    self.jobs["running"]) >= self.app.config.MAX_SIM_THREADS:
                await tornado.gen.sleep(
                    self.app.config.DEFAULT_QUEUE_CHECK_INTERVAL)
            self.jobs["queued"].popleft()

        self.jobs["running"].append(pid)
        out("Starting Job #{}".format(pid))
        logger.log("Starting Job #{}".format(pid))
        proc = self.executor.submit(run_job, command)
        exit_code = proc.result()

        self.jobs["running"].remove(pid)

        if exit_code is 0:
            out("Finished Job #{}".format(pid))
            logger.log("Finished Job #{}".format(pid))
            return pid
        else:
            out("Job #{} Failed".format(pid), "error")
            logger.log("Job #{} Failed".format(pid))
            raise ProcessFailureException

    def queue_job(self, pid, command):
        job = {"pid": pid, "command": command}
        self.jobs["queued"].append(job)
        logger.log("Job ", pid, " Queued.")
        return job
