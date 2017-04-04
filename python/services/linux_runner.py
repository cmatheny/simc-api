import subprocess

def get_simc_armory_to_json_command(locale, realm, character, id):
    armory_string = "".join(["armory=",",".join([locale, realm, character])])
    json_string = "".join(["json2=",str(id),".json"])
    call_list = ["simc", armory_string, json_string]
    return call_list

def run_command(proc):
    exit_code = subprocess.call(proc['command'])
    return exit_code
