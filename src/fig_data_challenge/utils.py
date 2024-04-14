import logging
from logging.handlers import RotatingFileHandler
def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

    file_handler = RotatingFileHandler('logs/fig_data_challenge.log', maxBytes=1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    logger.addHandler(console_handler)

    return logger