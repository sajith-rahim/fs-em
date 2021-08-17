import datetime
import logging
import os


class Logger:

    def __init__(self, directory='logs'):
        self.directory = directory
        self.file_name = 'base'
        self.default_level = 'DEBUG'

        self.create_folder(directory)

    def create_folder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print('Directory created. ' + directory)
        except OSError:
            print('Directory exists. ' + directory)

    def get_logger(self, level='DEBUG', file_name=None, do_print=False):
        """ """
        if file_name is None:
            file_name = self.file_name

        if level is None:
            level = self.default_level

        logger = logging.getLogger(file_name)
        logger.setLevel(getattr(logging, level))

        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s>>%(module)s:%(funcName)s: %(message)s', "%Y-%m-%d %H:%M:%S")

        stream_formatter = logging.Formatter(
            '%(levelname)s>>%(module)s:%(funcName)s: %(message)s')

        date = datetime.date.today()
        date = '%s-%s-%s' % (date.day, date.month, date.year)
        log_file_path = os.path.join(self.directory, '%s-%s.log' % (file_name, date))

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(stream_formatter)

        logger.addHandler(file_handler)
        if do_print:
            logger.addHandler(stream_handler)

        logger.propagate = False

        return logger
