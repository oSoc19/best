import logging

# Setup logger - (Python logger breaks PEP8 by default)
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
# file_handler logs to file, stream_handler to console
file_handler = logging.FileHandler('downloader.log')
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s : %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
