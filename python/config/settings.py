import sys

SERVER_PORT = "8888"

MAX_SIM_THREADS = 2
DEFAULT_QUEUE_CHECK_INTERVAL = 2
DEFAULT_THREAD_CHECK_INTERVAL = .2
DEFAULT_REGION = "us"

CONTROLLER_MODULES = [
    'rest_controllers',
    'socket_controllers',
]

# Logger config
logger_settings = {
    "DEFAULT_DEBUG": sys.stdout,
    "DEFAULT_LOG": sys.stdout,
    "DEFAULT_ERR": sys.stderr,
    "DEFAULT_WARN": sys.stderr,
    "INCLUDE": {
                "debug": True,
                "log": True,
                "err": True,
                "warn": True
                },
    "TIMESTAMP": True,
}
