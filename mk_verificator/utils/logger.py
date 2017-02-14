import os
import logging
import paramiko

from logging import StreamHandler
from logging.handlers import RotatingFileHandler


_log_dir = "/var/log/mk_verificator"

if not os.path.exists(_log_dir):
    os.mkdir(_log_dir)

# -------------------------------------------------------------
# paramiko logger
_paramiko_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
_paramiko_stream_logger = StreamHandler()
_paramiko_stream_logger.setFormatter(_paramiko_formatter)
_paramiko_stream_logger.setLevel(logging.WARN)
_paramiko_log_file = os.path.join(_log_dir, "paramiko.log")
_paramiko_file_logger = RotatingFileHandler(
    _paramiko_log_file,
    mode='a', maxBytes=1 << 20, backupCount=2
)
_paramiko_file_logger.setFormatter(_paramiko_formatter)
_paramiko_file_logger.setLevel(logging.DEBUG)
_paramiko_logger = paramiko.util.logging.getLogger("paramiko")
_paramiko_logger.setLevel(logging.DEBUG)
_paramiko_logger.addHandler(_paramiko_stream_logger)
_paramiko_logger.addHandler(_paramiko_file_logger)


# -------------------------------------------------------------
# mk_verificator logger
_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - \
    [%(filename)s:%(lineno)s - %(funcName)s() ] - %(message)s'
)
_stream_logger = StreamHandler()
_stream_logger.setFormatter(_formatter)
_stream_logger.setLevel(logging.INFO)
_log_file = os.path.join(_log_dir, "run.log")
_file_logger = RotatingFileHandler(
    _log_file,
    mode='a', maxBytes=1 << 20, backupCount=2
)
_file_logger.setFormatter(_formatter)
_file_logger.setLevel(logging.DEBUG)
_logger = logging.getLogger("mk_verificator")
_logger.setLevel(logging.DEBUG)
_logger.addHandler(_stream_logger)
_logger.addHandler(_file_logger)


def getLogger(name):
    return logging.getLogger(name)


__all__ = ["getLogger"]
