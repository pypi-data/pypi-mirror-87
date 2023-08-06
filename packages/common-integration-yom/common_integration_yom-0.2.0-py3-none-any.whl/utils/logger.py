"""
Module for log all the messages in the same format
"""
import sys
import logging
import bunyan
from singleton import Singleton

class Logger(metaclass=Singleton):
    """
    Class for log porpuse
    """

    def __init__(self, name):
        self.logger = None
        self.flag = {'batch_log': True}
        self.set_logger(name)

    def set_logger(self, name):
        """
        Configure the logger
        """
        self.logger = logging.getLogger(name)
        log_handler = logging.StreamHandler(stream=sys.stdout)
        formatter = bunyan.BunyanFormatter()
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logging.DEBUG)

    def build_extra(self, metadata):
        """
        Takes a dictionary of information and builds
        the payload to be logged by the logger (aside of the message).
        Args:
            metadata(dict): dictionary of metadata related to the event logged.
        Returns:
            (dict): dictionary of extra data to be logged
        """
        if isinstance(metadata, dict):
            return {**self.flag, "metadata": metadata}
        return self.flag

    def debug(self, message, metadata=None):
        """
        Log a message on JSON format for debbuging
        This will log json with level 20
        Args:
            message (string): Message to be log
            metadata(dict): This module extends this functionality by allowing an extra keyword arg,
            and passing a dictionary.
        """
        extra = self.build_extra(metadata)
        self.logger.debug(message, extra=extra)

    def info(self, message, metadata=None):
        """
        Log a message on JSON format to deliver information about a process
        This will log json with level 30
        Args:
            message (string): Message to be log
            metadata(dict): This module extends this functionality by allowing an extra keyword arg,
            and passing a dictionary.
        """
        extra = self.build_extra(metadata)
        self.logger.info(message, extra=extra)

    def warning(self, message, metadata=None):
        """
        Log a message on JSON format for warning propuse.
        This will log json with level 40
        Args:
            message (string): Message to be log
            metadata(dict): This module extends this functionality by allowing an extra keyword arg,
            and passing a dictionary.
        """
        extra = self.build_extra(metadata)
        self.logger.warning(message, extra=extra)

    def error(self, message, metadata=None):
        """
        Log a message on JSON format for error propuse.
        This will log json with level 50
        Args:
            message (string): Message to be log
            metadata(dict): This module extends this functionality by allowing an extra keyword arg,
            and passing a dictionary.
        """
        extra = self.build_extra(metadata)
        self.logger.error(message, extra=extra)

    def critical(self, message, metadata=None):
        """
        Log a message on JSON format for critical errors.
        This will log json with level 60
        Args:
            message (string): Message to be log
            metadata(dict): This module extends this functionality by allowing an extra keyword arg,
            and passing a dictionary.
        """
        extra = self.build_extra(metadata)
        self.logger.critical(message, extra=extra)

    def exception(self, message, metadata=None):
        """
        Convenience method for logging an ERROR with exception information
        This will log json with level 50
        Args:
            message (string): Message to be log
            metadata(dict): This module extends this functionality by allowing an extra keyword arg,
            and passing a dictionary.
        """
        extra = self.build_extra(metadata)
        self.logger.exception(message, extra=extra)