from config import settings
from services import linux_runner as runner
from services.process_manager import ProcessManager
from utils import file_manager


class SimcService():

    def __init__(self):
        self.proc_man = ProcessManager()

    def simc_armory_to_json(self, char_json):

        id = char_json["id"] if "id" in char_json \
            else self.proc_man.generate_random_id()

        region = char_json["region"] if "region" in char_json \
            else settings.DEFAULT_REGION

        command = runner.get_simc_armory_to_json_command(
                region, char_json['realm'], char_json['name'], id)

        job = self.proc_man.queue_process_and_wait(id, command)

        results_file = "".join([str(id), ".json"])
        file_manager.check_for_file(results_file)
        results_json = file_manager.load_json(results_file)

        self.cleanup(results_file, job)
        return results_json

    def cleanup(self, results_file, job):
        file_manager.remove_file(results_file)
        self.proc_man.cleanup_completed_job(job)

    def get_queue(self):
        return self.proc_man.jobs

    def check_dict_keys(dictionary, keylist, exception=False):
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
