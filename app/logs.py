import os
import logging
from logging.handlers import TimedRotatingFileHandler

log_directory = "logs"

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

global_logger = logging.getLogger()

debug_log_file_path = os.path.join(log_directory, 'app-debug.log')
info_log_file_path = os.path.join(log_directory, 'app-info.log')
warn_log_file_path = os.path.join(log_directory, 'app-warn.log')
error_log_file_path = os.path.join(log_directory, 'app-error.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler_debug = TimedRotatingFileHandler(debug_log_file_path, when='midnight', interval=1, backupCount=30)
handler_debug.setLevel(logging.DEBUG)
handler_debug.setFormatter(formatter)

handler_info = TimedRotatingFileHandler(info_log_file_path, when='midnight', interval=1, backupCount=30)
handler_info.setLevel(logging.INFO)
handler_info.setFormatter(formatter)



handler_warn = TimedRotatingFileHandler(warn_log_file_path, when='midnight', interval=1, backupCount=30)
handler_warn.setLevel(logging.WARN)
handler_warn.setFormatter(formatter)

handler_err = TimedRotatingFileHandler(error_log_file_path, when='midnight', interval=1, backupCount=30)
handler_err.setLevel(logging.ERROR)
handler_err.setFormatter(formatter)

global_logger.addHandler(handler_debug)
global_logger.addHandler(handler_info)
global_logger.addHandler(handler_warn)
global_logger.addHandler(handler_err)

global_logger.info("logger init completed.")
