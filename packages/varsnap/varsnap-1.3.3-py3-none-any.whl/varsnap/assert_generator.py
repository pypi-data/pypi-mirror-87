import logging
import json
import sys

from qualname import qualname
import requests
from typing import List, Optional, Tuple

from . import core


TRIAL_GROUP_URL = 'https://www.varsnap.com/api/trial_group/'


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


def generate_trial_group() -> str:
    data = {
        'consumer_token': core.env_var(core.ENV_CONSUMER_TOKEN),
    }
    response = requests.post(TRIAL_GROUP_URL, data=data)
    try:
        response_data = json.loads(response.content)
    except json.decoder.JSONDecodeError:
        response_data = {}
    if not response_data or response_data['status'] != 'ok':
        trial_group_id = ''
    else:
        trial_group_id = response_data['trial_group_id']
    return trial_group_id


def _test(test_logger: logging.Logger) -> List[core.Trial]:
    trial_group_id = generate_trial_group()
    all_trials: List[core.Trial] = []
    for consumer in core.CONSUMERS:
        consumer_name = qualname(consumer.target_func)
        test_logger.info("Running Varsnap tests for %s" % consumer_name)
        all_trials += consumer.consume(trial_group_id)
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
