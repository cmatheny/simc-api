import math
from concurrent.futures import ThreadPoolExecutor
import random
import subprocess
import collections

import tornado.ioloop
import tornado.process
import tornado.gen

from exceptions.exceptions import SimulationFailureException
from utils import file_manager, logger
from services import linux_runner as runner
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
            'completed': []
        }
        self.app = Application()
        self.executor = ThreadPoolExecutor(max_workers=2)

#        self.threads = []
#        self.thread_pid_counter = 1
#        self.monitor = ProcessMonitor(self.jobs, self.threads)
#        self.monitor.start()
#        for i in range(settings.MAX_SIM_THREADS):
#            self.start_thread()

    def generate_random_pid(self):
        while True:
            pid = math.floor(random.random() * 9999999)
            if not (any(proc == pid for proc in self.jobs["queued"]) and
                    any(proc == pid for proc in self.jobs["running"]) and
                    any(proc == pid for proc in self.jobs["completed"])):
                return pid

    async def run_job(self, pid, command, out=logger.null):

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
        proc = self.executor.submit(run_job, command)
        logger.log(proc.done())
        while not proc.done():
            await tornado.gen.sleep(1)
            logger.log(proc.done())

#        proc = tornado.process.Subprocess(command)
#        await proc.wait_for_exit()

        self.jobs["running"].remove(pid)
        self.jobs["completed"].append(pid)

    def queue_job(self, pid, command):
        job = {"pid": pid, "command": command}
        self.jobs["queued"].append(job)
        logger.log("Job ", pid, " Queued.")
        return job

#    def wait_for_job(self, job,
#                     interval=app.settings.DEFAULT_QUEUE_CHECK_INTERVAL):
#
#        while job not in self.jobs["completed"]:
#            time.sleep(interval)
#
#    def queue_process_and_wait(self, pid, command,
#                               interval=settings.DEFAULT_QUEUE_CHECK_INTERVAL):
#        job = self.queue_job(pid, command)
#        self.wait_for_job(job, interval)
#        return job
#
#    def verify_process_success(self, process):
#        if process['exit_code'] is not 0:
#            raise SimulationFailureException(
#                "Simulation dpid not complete successfully")
#
#    def cleanup_completed_job(self, job):
#        self.jobs["completed"].remove(job)

#
#class ProcessMonitor(threading.Thread):
#
#    def __init__(self, jobs, threads):
#        threading.Thread.__init__(self)
#        self.jobs = jobs
#        self.threads = threads
#
#    def run(self):
#        while True:
#            self.print_jobs()
#            time.sleep(1)
#            self.print_threads()
#            time.sleep(4)
#
#    def print_jobs(self):
#        logger.log(self.jobs)
#
#    def print_threads(self):
#        for thread in self.threads:
#            logger.log('{"threadpid": ', str(thread.threadpid),
#                       ', "status": ', thread.status,
#                       ', "completed_jobs": ', str(thread.completed_jobs), '}')


class ProcessThread:

    def __init__(self, threadpid, jobs):
        self.threadpid = threadpid
        self.jobs = jobs
        self.completed_jobs = 0
        self.status = "Initialized"
        self.is_running = False

    def run_job(self, proc):
        logger.log("Starting Simulation Thread ", str(self.threadpid))
        return subprocess.call(proc)

    def stop(self):
        pass

    def __str__(self):
        return ("{'threadpid': '{}', 'status': '{}', 'completed_jobs': '{}'}".
                format(self.threadpid, self.status, self.completed_jobs))
