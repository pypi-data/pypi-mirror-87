import logging

from .logger_json import JsonFormatter

try:
    from concurrent_log_handler import ConcurrentRotatingFileHandler as RotatingFileHandler
except Exception as e:
    from logging.handlers import RotatingFileHandler


class LogJsonFormat:
    SUPPORTED_KEYS = [
        'asctime', 'process', 'funcName', 'module', 'processName', 'pathname', 'lineno', 'msecs', 'filename', 'project',
        'thread', 'created', 'threadName', 'levelname', 'name', 'relativeCreated', 'host', 'message'
    ]

    def __init__(self, file_path, console=False, project=None):

        # log_handler = logging.FileHandler(filename=file_path, mode='a', encoding='U8')

        formatter = JsonFormatter(
            ' '.join(['%({0:s})'.format(i) for i in self.SUPPORTED_KEYS]),
            json_ensure_ascii=False,
            project=project
        )
        logger = logging.getLogger()
        logger.handlers = []
        logger.setLevel(logging.INFO)

        if file_path:
            import os
            if os.path.exists(os.path.dirname(file_path)):
                pass
            else:
                os.makedirs(os.path.dirname(file_path))
            log_handler = RotatingFileHandler(filename=file_path, backupCount=10, mode='a', encoding='U8',
                                              maxBytes=1024 * 1024 * 520)
            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)
        if console:
            handler_console = logging.StreamHandler()
            handler_console.setLevel(logging.INFO)
            handler_console.setFormatter(formatter)
            logger.addHandler(handler_console)
