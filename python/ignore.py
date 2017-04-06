import datetime
import multiprocessing
import types
import subprocess

from tornado.websocket import WebSocketHandler
import tornado.process
import tornado.gen

from utils import file_manager
import services.linux_runner as runner
from utils.logger import log, warn



class Test:
    a = 5
    b = 2
    print("Imported it")

    @classmethod
    def callit(cls, x):
        print("Called it")
        return cls.a + x / cls.b


async def long_run(delay, out=log):

    for i in range(delay):
        log(delay-i)
        out("Starting in {}".format(delay-i))
        await tornado.gen.sleep(1)

    out("Starting Sim")
    proc = runner.get_simc_armory_to_json_command("us", "emerald-dream",
                                                  "sarrial", 510)

    job = multiprocessing.Process(target=worker, args=(proc,))
    job.start()

    while True:
        try:
            file_manager.load_json("510.json")
            break
        except FileNotFoundError:
            await tornado.gen.sleep(1)

    out("Done")
    out(file_manager.load_json("510.json"))

    file_manager.remove_file("510.json")

def worker(proc):
    return subprocess.call(proc)
