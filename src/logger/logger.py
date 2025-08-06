import logging

def setup_logger(log_file="app.log"):
    logging.basicConfig(
        filename=log_file,
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.INFO,
        filemode='a'
    )
    logger = logging.getLogger(__name__)
    return logger