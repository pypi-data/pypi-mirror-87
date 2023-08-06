import logging
import sys

from qualname import qualname
from typing import List, Optional, Tuple

from . import core


def _configure_logger() -> logging.Logger:
    varsnap_logger = logging.getLogger(core.__name__)
    varsnap_logger.handlers = []
    varsnap_logger.disabled = True
    varsnap_logger.propagate = False

    test_logger = logging.getLogger(__name__)
    test_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    test_logger.addHandler(handler)
    return test_logger


def _test(test_logger: logging.Logger) -> List[core.Trial]:
    all_trials: List[core.Trial] = []
    for consumer in core.CONSUMERS:
        consumer_name = qualname(consumer.target_func)
        test_logger.info("Running Varsnap tests for %s" % consumer_name)
        all_trials += consumer.consume()
    return all_trials


def test() -> Tuple[Optional[bool], str]:
    test_logger = _configure_logger()
    trials = _test(test_logger)
    all_matches: Optional[bool] = None
    if trials:
        all_matches = all([t.matches for t in trials])
    all_logs = "\n\n".join([
        t.report for t in trials if t.report and not t.matches
    ])
    return all_matches, all_logs
