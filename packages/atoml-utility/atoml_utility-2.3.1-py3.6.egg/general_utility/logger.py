import logging
from . import utils as us

################################################################################

class logger():
    def __init__(self, logfilename, logconsole = True, appname = "", level = "info"):
        us.check_path_exists(logfilename)

        if len(appname) <= 0: appname = __name__

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        level = self.get_level(level)

        self.logger = logging.getLogger(appname)

        fh = logging.FileHandler(logfilename)
        fh.setFormatter(formatter)
        fh.setLevel(level)
        self.logger.addHandler(fh)

        if (logconsole):
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            ch.setLevel(level)
            self.logger.addHandler(ch)

    def get_level(self, level = "info"):
        if (level.upper() == "DEBUG"):
            return logging.DEBUG
        if (level.upper() == "INFO"):
            return logging.INFO
        if (level.upper() == "WARNING"):
            return logging.WARNING
        if (level.upper() == "ERROR"):
            return logging.ERROR
        if (level.upper() == "CRITICAL"):
            return logging.CRITICAL

    ####################################################

    def output(self, log, level = "info"):
        print(log)
        if (level.upper() == "DEBUG"):
            self.logger.debug(log)
        if (level.upper() == "INFO"):
            self.logger.info(log)
        if (level.upper() == "WARNING"):
            self.logger.warning(log)
        if (level.upper() == "ERROR"):
            self.logger.error(log)
        if (level.upper() == "CRITICAL"):
            self.logger.critical(log)

    ####################################################