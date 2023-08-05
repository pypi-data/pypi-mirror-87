import logging
from rich.logging import RichHandler

NELL_FILE = '/dev/null'


def logger(filename: str = NELL_FILE):
    FORMAT = "[line %(lineno)d] %(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(
            level="NOTSET",
            format=FORMAT,
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=filename
    )
    log = logging.getLogger("rich")
    return log


defaultLogger = logger()
