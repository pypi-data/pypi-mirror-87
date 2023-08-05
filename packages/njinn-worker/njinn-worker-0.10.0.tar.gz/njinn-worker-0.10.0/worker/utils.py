import logging
import os
import sys
from time import sleep

log = logging.getLogger(__name__)


def is_windows():
    return sys.platform.startswith("win")


def get_worker_version() -> str:
    version_file = open(os.path.join(os.path.dirname(__file__), "VERSION"))
    return version_file.read().strip()


def read_stdout(proc, lines):
    """ Reads all remaining stdout """
    if proc and proc.stdout:
        while True:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None:
                return
            log.debug("Action stdout: %s", line.rstrip())
            lines.append(line)
    return None


# 24h is also equal to the maximum task timeout
MAXIMUM_API_REQUEST_RETRY_DURATION_SECONDS = 24 * 3600
# max. 5 minutes between attempts
MAXIMUM_API_REQUEST_WAIT_TIME_SECONDS = 300


def api_response_predicate(r):
    """
    Currently, we retry on
    502 Bad Gateway
    503 Service Unavailable
    504 Gateway Timeout
    """

    return r.status_code in [502, 503, 504]


def setup_backoff_handler(handler=None):
    bl = logging.getLogger("backoff")
    if len([h for h in bl.handlers if not isinstance(h, logging.NullHandler)]) == 0:
        if handler is None:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "[%(asctime)s %(levelname)s/%(threadName)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
        logging.getLogger("backoff").addHandler(handler)
