from utils.file_manager import FileManager

SERVER_PORT = "28888"

MAX_SIM_THREADS = 2
DEFAULT_QUEUE_CHECK_INTERVAL = 2
DEFAULT_THREAD_CHECK_INTERVAL = .2
DEFAULT_REGION = "us"

CONTROLLER_MODULES = [
    'rest_controllers',
    'socket_controllers',
]

# Logger config
fm = FileManager()
logger_settings = {
    "DEFAULT_DEBUG": fm.stdout,
    "DEFAULT_LOG": fm.stdout,
    "DEFAULT_ERR": fm.stderr,
    "DEFAULT_WARN": fm.stderr,
    "DEFAULT_NULL": fm.null,
    "INCLUDE": {
                "debug": False,
                "log": True,
                "err": True,
                "warn": True,
                "null": True,
                },
    "TIMESTAMP": True,
}
