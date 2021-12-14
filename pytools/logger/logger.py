import logging

# Creqte and configure a logger
LOG_FORMAT = "%(levelname)s - %(asctime)s, %(lineno)d: %(message)s"
# Log to file that overwrites at every run
# logging.basicConfig(filename="model.log",
#                     level=logging.INFO,
#                     format=LOG_FORMAT,
#                     filemode='w')

# Log to stdout
logging.basicConfig(format=LOG_FORMAT,
                    level=logging.INFO,
                    datefmt='%a, %d %b %Y %H:%M:%S')

log = logging.getLogger(__name__)
