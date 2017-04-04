import sys

SERVER_NAME = None
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
    "LOG_INCLUDE": [ "debug", "log", "err", "warn" ],
    "LOG_TIMESTAMP": True,
}
