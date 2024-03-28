import sys
import time
from utils.paths import LOG_PATH

def init_logging(logging, filename, source = None):
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)

    LOG_TIME = time.asctime().replace(' ', '_').replace(':', '-')
    logging.basicConfig(
        filename=LOG_PATH / f'{LOG_TIME}-{filename}.txt',
        format='%(levelname)s:%(message)s',
        level=logging.DEBUG
    )
    if source:
        logging.info(f'Started {source} logging successfully.')

def is_linux():
    return 'linux' in sys.platform

def is_windows():
    return 'win32' in sys.platform

if is_linux():
    from .linux import *
elif is_windows():
    from .windows import *
else:
    raise RuntimeError('Unsupported operating system: {}'.format(sys.platform))
