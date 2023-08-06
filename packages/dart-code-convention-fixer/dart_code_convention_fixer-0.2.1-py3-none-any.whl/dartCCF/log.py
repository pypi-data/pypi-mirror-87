import logging


def setup_logger(logger_file_name):
    logger = logging.getLogger('DSCA')
    logger.setLevel(logging.DEBUG)

    console_stream_handler = logging.StreamHandler()
    console_stream_handler.setLevel(logging.DEBUG)
    console_stream_handler.setFormatter(logging.Formatter(fmt='%(levelname)s - %(message)s'))

    logger.addHandler(console_stream_handler)

    file_handler = logging.FileHandler(filename='./%s' % logger_file_name, mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s - %(message)s'))

    logger.addHandler(file_handler)
