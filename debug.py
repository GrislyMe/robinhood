from enum import Enum
import logging

class Error(Enum):
    LOGIN_FAIL = 1
    NO_SESSION_ID = 2
    EXCEPTION_FATAL = 3
    EXCEPTION_NON_FATAL = 4
    LOG_FILE_WRITE_FAIL = 5
    POST_REQUEST_FAIL = 6
    GET_REQUEST_FAIL = 7
    NO_FORM_IN_PAGE = 8
    NO_TABLE_IN_FORM = 9
    EMPTY_TABLE = 10

def logger_init(enable_log = True, enable_debug = False):
    if enable_log:
        LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
        DATE_FORMAT = '%m/%d %H:%M:%S'
        if enable_debug:
            LOGGING_FORMAT += " in { %(funcName)s: %(lineno)s }"
            logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
        else:
            logging.basicConfig(level=logging.WARNING, format=LOGGING_FORMAT, datefmt=DATE_FORMAT)

    return 0

