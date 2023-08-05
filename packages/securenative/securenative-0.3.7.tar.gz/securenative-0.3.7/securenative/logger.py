import logging


class Logger(object):
    logger = logging.getLogger()

    @staticmethod
    def init_logger(level):
        logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    @staticmethod
    def info(msg):
        Logger.logger.info(msg)

    @staticmethod
    def debug(msg):
        Logger.logger.debug(msg)

    @staticmethod
    def warning(msg):
        Logger.logger.warning(msg)

    @staticmethod
    def error(msg):
        Logger.logger.error(msg)
