import logging
import sys


def get_logger(name=None, level="INFO"):
    """ A helper function to setup and return a logger object."""
    logger = logging.getLogger(name)
    fh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(level)
    
    return logger
