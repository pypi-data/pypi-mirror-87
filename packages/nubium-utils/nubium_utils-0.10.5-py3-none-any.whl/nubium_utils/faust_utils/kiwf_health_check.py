import sys
from logging import getLogger
from collections import deque
from nubium_utils import init_logger
from nubium_utils.faust_utils.faust_runtime_vars import default_env_vars


def kiwf_log_analysis():
    lines_to_tail = 10
    last_lines = deque(open(default_env_vars()['KIWF_LOG_FILEPATH']), lines_to_tail)
    errors = [error_string for error_string in default_env_vars()['KIWF_ERROR_STRINGS'].split(',') if
              error_string in str(last_lines)]

    if errors:
        init_logger(__name__)
        LOGGER = getLogger(__name__)
        LOGGER.error(f"KIWF encountered error(s): [{', '.join(errors)}].\nKilling Pod.")
        sys.exit(1)
