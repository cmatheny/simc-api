import tornado.ioloop

from services.application import Application
from services.process_manager import ProcessManager
from utils import file_manager, logger
from utils.misc import singleton


@singleton
class SimcService():

    def __init__(self):
        self.proc_man = ProcessManager()
        self.app = Application()

    def get_simc_armory_to_json_command(self, locale, realm, character, id):
        armory_string = "armory={},{},{}".format(locale, realm, character)
        json_string = "json2={}.json".format(id)
        call_list = ["simc", armory_string, json_string, "threads=2", "iterations=10000"]
        return call_list

    def simc_armory_to_json(self, char_json, out=logger.warn):

        self.check_dict_keys(char_json, ['realm', 'name'], True)

        pid = self.proc_man.generate_random_pid()
        region = char_json["region"] if "region" in char_json \
            else self.app.config.DEFAULT_REGION

        command = self.get_simc_armory_to_json_command(
                region, char_json['realm'], char_json['name'], pid)

        tornado.ioloop.IOLoop.current().spawn_callback(
                self.run_simulation, pid, command, out)

    async def run_simulation(self, pid, command, out=logger.warn):

        await self.proc_man.run_job(command, pid, out)

        results_file = "{}.json".format(pid)
        results_json = file_manager.load_json(results_file)
        out(results_json, "result")

        file_manager.remove_file(results_file)

    def get_queue(self):
        return self.proc_man.jobs

    def check_dict_keys(self, dictionary, keylist, exception=False):
        missing_keys = []
        check = True
        missing_keys = [key for key in keylist if key not in dictionary]
        check = True if len(missing_keys) is 0 else False

        if check or not exception:
            return check

        else:
            if len(missing_keys) is 1:
                message = "Missing required field: '{}'".format(
                        missing_keys[0])
            else:
                message = "Missing required fields: ['{}']".format(
                        "".join(missing_keys))
            raise KeyError(message)
