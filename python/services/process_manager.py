import math
from concurrent.futures import ThreadPoolExecutor
import random
import subprocess
import collections

import tornado.gen

import exceptions.exceptions as ex
from utils import logger
from services.application import Application


def run_job(pid, job, out=logger.warn):
    logger.log("Starting Simulation Thread.")
    logger.log(job["command"])
    process = subprocess.Popen(job["command"], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True)
    for line in iter(process.stdout.readline, ''):
        if job["kill"] is True:
            process.kill()
            raise ex.CancelledSimulationException
        message = {
                "job_id": pid,
                "message": '{}'.format(line.rstrip())
                }
        logger.debug(message)
        out(message, "output")
    process.wait()
    return process.returncode


class ProcessManager:

    def __init__(self):
        self.jobs = {
            'queued': collections.deque(),
            'running': [],
        }
        self.app = Application()
        self.executor = ThreadPoolExecutor(max_workers=20)

    def generate_random_pid(self):
        while True:
            pid = math.floor(random.randrange(100000, 999999))
            if not (any(proc == pid for proc in self.jobs["queued"]) and
                    any(proc == pid for proc in self.jobs["running"])):
                return pid

    async def run_job(self, command, pid=None, out=logger.warn):

        pid = pid if pid else self.generate_random_pid()

        await self.wait_for_queue(pid, out)

        job = {"pid": pid, "executor": None, "command": command, "kill": False}
        self.jobs["running"].append(job)
        out({"job_id": pid, "status": "Running"}, "status")
        logger.log("Starting Job #{}".format(pid))
        proc = self.executor.submit(run_job, pid, job, out)
        job["executor"] = proc

        while proc.running():
            await tornado.gen.sleep(1)

        exit_code = proc.result()

        self.jobs["running"].remove(job)

        if exit_code is 0:
            out({"job_id": pid, "status": "Completed"}, "status")
            logger.log("Finished Job #{}".format(pid))
            return pid
        else:
            out({"job_id": pid, "status": "Failed"}, "status")
            out("Job #{} Failed".format(pid), "error")
            logger.log("Job #{} Failed".format(pid))
            raise ex.ProcessFailureException

    async def wait_for_queue(self, pid, out=logger.warn):

        if len(self.jobs["running"]) >= self.app.config.MAX_SIM_THREADS:
            self.jobs["queued"].append(pid)
            logger.log(self.jobs)
            out({"job_id": pid, "status": "Queued",
                 "position": len(self.jobs["queued"])}, "status")
            while self.jobs["queued"][0] is not pid or len(
                    self.jobs["running"]) >= self.app.config.MAX_SIM_THREADS:
                await tornado.gen.sleep(
                    self.app.config.DEFAULT_QUEUE_CHECK_INTERVAL)
            return self.jobs["queued"].popleft()

    def cancel_job(self, pid):
        if pid in self.jobs["queued"]:
            self.jobs["queued"].remove(pid)
        else:
            job = next((job for job in self.jobs["running"]
                       if job["pid"] == pid), None)
            if job:
                logger.log(self.jobs["running"])
                job["kill"] = True
                logger.log(job["executor"].cancelled())
                self.jobs["running"].remove(job)
