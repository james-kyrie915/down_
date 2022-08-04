import os
import datetime
from loguru import logger


class Log(object):

    def __init__(self, log_file):
        # self.day = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.day = datetime.datetime.now().strftime('%Y-%m-%d')
        self.log_dir = "E:/Pycharm_file/Data_collection/para/log/" + self.day
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_path = self.log_dir + '/' + log_file + '.log'
        logger.add(self.log_path)

    @staticmethod
    def debug(massage):
        logger.debug(massage)

    @staticmethod
    def warning(massage):
        logger.warning(massage)

    @staticmethod
    def error(massage):
        logger.error(massage)

    @staticmethod
    def info(massage):
        logger.info(massage)

#
# if __name__ == '__main__':
#     log = Log()
