import logging
from logging.handlers import RotatingFileHandler

class FileLogger():
    """
    Thin wrapper around python logging module to use rotateing file logger. 
    provide two inputs: logfile and level; to init instance of logger. 
    Optional inputs: maxBytes = 102400, backupCount = 2;
    level: debug, info, warning, error, critical
    then use logger.debug(msg) / logger.info(msg) etc to write a log. 
    """

    def __init__(self, logfile="", level="INFO", maxBytes=102400, backupCount=2):
        """
        running_log: the file to write logs to.
        the logger have 5 different levels. [debug, info, warning, error, critical]
        use logger.[debug]('msg') to log a message.
        """
        level = getattr(logging, level.upper(),20)
        logger=logging.getLogger('Monitor')
        logger.setLevel(level)
        fh = RotatingFileHandler(
            logfile, maxBytes=maxBytes, backupCount=backupCount)
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p'
        ))
        logger.addHandler(fh)
        self.logger=logger

        for i in ['debug','info','warning','error','critical']:
            setattr(self,i,getattr(self.logger,i))

    
