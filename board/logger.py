import os
import logging
from logging import handlers


class boardLogger():
    logFileName = ''
    loggerName = ''
    logDir = ''
    logInstance = None

    @staticmethod
    def create_logger():
        logger = logging.getLogger(boardLogger.loggerName)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if not logger.handlers:
            if not os.path.exists(boardLogger.logDir):
                os.makedirs(boardLogger.logDir)
            handler = logging.handlers.RotatingFileHandler(boardLogger.logDir + boardLogger.logFileName,
                                                           maxBytes=(1048576 * 10), backupCount=9)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        boardLogger.logInstance = logger
        return logger

    @staticmethod
    def loggerInit(loggerName, fileName, logDirName):
        boardLogger.logFileName = fileName
        boardLogger.loggerName = loggerName
        if len(str(logDirName).strip()) == 0:
            boardLogger.logDir = './'
        elif not str(logDirName).strip().endswith('/'):
            boardLogger.logDir = logDirName + "/"
        else:
            boardLogger.logDir = logDirName

    @staticmethod
    def getInstance():
        if boardLogger.logInstance == None:
            boardLogger.create_logger()

        return boardLogger.logInstance