import inspect
from config.settings import logger_settings as settings
import datetime


def print_log(*args, log_type, file, separator, end):
    
    last_frame = inspect.stack()[2]
    
    caller = "{} in {}, line {}:".format(last_frame.function, 
            last_frame.filename, last_frame.lineno)
    
    output = "".join('{}'.format(arg) for arg in args)
    
    full_output = "---{}:\t{}\t{}\n\t{}\n".format(log_type, timestamp(),
            caller, output)
    
    print(full_output, file=file, sep=separator, end=end, flush=True)

def debug(*args, file=settings["DEFAULT_DEBUG"], separator="", end="\n"):
    
    if 'debug' in settings["LOG_INCLUDE"]:
        print_log(*args, log_type="DEBUG", file=file,
                separator=separator, end=end)

def log(*args, file=settings["DEFAULT_LOG"], separator="", end="\n"):
    
    if 'log' in settings["LOG_INCLUDE"]:
        print_log(*args, log_type="LOG", file=file,
                separator=separator, end=end)


def err(*args, file=settings["DEFAULT_ERR"], separator="", end="\n"):
    
    if 'err' in settings["LOG_INCLUDE"]:
        print_log(*args, log_type="ERROR", file=file,
                separator=separator, end=end)


def warn(*args, file=settings["DEFAULT_WARN"], separator="", end="\n"):
    
    if 'warn' in settings["LOG_INCLUDE"]:
        print_log(*args, log_type="WARNING", file=file,
                separator=separator, end=end)


def timestamp():
    
    if settings["LOG_TIMESTAMP"] is True:
        return str(datetime.datetime.now())
    else:
        return ""
        
