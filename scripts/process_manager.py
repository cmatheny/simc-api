import collections
import exceptions
import linux_runner as runner
import math
import random
import settings
import sys
import time
import threading

class ProcessManager():
    
    def __init__(self):
        self.jobs = {
            'queued': collections.deque(),
            'running': [],
            'completed': []
        }
        self.threads = []
        self.thread_id_counter = 1
        self.monitor = ProcessMonitor(self.jobs, self.threads)
        self.monitor.start()
        for i in range(settings.MAX_SIM_THREADS):
            self.start_thread()

    def generate_random_id(self):
        while True:
            id = math.floor(random.random() * 9999999)
            if not (any(proc['id'] == id for proc in self.jobs["queued"]) and 
                    any(proc['id'] == id for proc in self.jobs["running"]) and
                    any(proc['id'] == id for proc in self.jobs["completed"])):
                return id

    def start_thread(self):
        thread = ProcessThread(self.thread_id_counter, self.jobs)
        self.threads.append(thread)
        self.thread_id_counter += 1
        thread.start()
        
    def stop_thread(self, thread_index):
        self.threads[thread_index].is_running = False
        
    def queue_job(self, id, command):
        job = {"id": id, "command": command}
        self.jobs["queued"].append(job)
        print("Simulation " + str(id) + " Queued.", file = sys.stderr)
        return job

    def wait_for_job(self, job, interval=settings.DEFAULT_QUEUE_CHECK_INTERVAL):
        while job not in self.jobs["completed"]:
            time.sleep(interval)
            
    def queue_process_and_wait(self, id, command,
                interval=settings.DEFAULT_QUEUE_CHECK_INTERVAL):
        job = self.queue_job(id, command)
        self.wait_for_job(job, interval)
        return job

    def verify_process_success(self, process):
        if process['exit_code'] is not 0:
            raise SimulationFailureException(
                "Simulation did not complete successfully")
                
    def cleanup_completed_job(self, job):
        self.jobs["completed"].remove(job)

class ProcessMonitor(threading.Thread):
    
    def __init__(self, jobs, threads):
        threading.Thread.__init__(self)
        self.jobs = jobs
        self.threads = threads
    
    def run(self):
        while True:
            self.print_jobs()
            time.sleep(1)
            self.print_threads()
            time.sleep(4)
        
    def print_jobs(self):
        print(self.jobs, file = sys.stderr)
    
    def print_threads(self):
        for thread in self.threads:
            print('{"threadID": ' + str(thread.threadID) + ', "status": ' + thread.status 
                + ', "completed_jobs": ' + str(thread.completed_jobs) + '}', file = sys.stderr)
        
class ProcessThread(threading.Thread):

    def __init__(self, threadID, jobs):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.jobs = jobs
        self.completed_jobs = 0
        self.status = "Initialized"
        self.is_running = False

    def run(self):
        print("Starting Simulation Thread " + str(self.threadID), file = sys.stderr)
        
        self.is_running = True
        self.status = "Idle"
        
        while self.is_running is True:
            if len(self.jobs["queued"]) is 0:
                time.sleep(settings.DEFAULT_THREAD_CHECK_INTERVAL)
            else:
                self.status = "Working"
                proc = self.jobs["queued"].popleft()
                
                self.jobs["running"].append(proc)
                exit_code = runner.run_command(proc)
                self.jobs["running"].remove(proc)
                
                proc['exit_code'] = exit_code
                self.jobs["completed"].append(proc)
                self.completed_jobs += 1
                print("Completed Simulation (" + str(self.completed_jobs) + ")",
                    file = sys.stderr)
                self.status = "Idle"
        
        self.status = "Stopped"
        
    def __str__(self):
        return ('{"threadID": ' + self.threadID + ', "status": ' + self.status 
                + ', "completed_jobs": ' + self.completed_jobs + '}')
