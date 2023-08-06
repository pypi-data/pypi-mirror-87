import os
import requests
import unittest

from varsnap import assert_generator, core
from varsnap.tests.test_assert_generator import mock_logger
from typing import Callable, Dict, List, Optional, Union, cast


def generate_reference_function() -> Callable[[int, int], int]:
    def example(x: int, y: int) -> int:
        return x * y
    example.__qualname__ = 'example'
    return example


def generate_test_function() -> Callable[[int, int], int]:
    def example(x: int, y: int) -> int:
        return x * y + 1
    example.__qualname__ = 'example'
    return example


class Example():
    add_producer: Optional[core.Producer] = None
    add_consumer: Optional[core.Consumer] = None
    subtract_producer: Optional[core.Producer] = None
    subtract_consumer: Optional[core.Consumer] = None

    def __init__(self, x: int):
        self.x = x

    def __repr__(self) -> str:
        return "<Example x=%s>" % self.x

    @core.varsnap
    def add(self, y: int) -> int:
        self.x += y
        return self.x

    @core.varsnap
    @staticmethod
    def subtract(x: int, y: int) -> int:
        return x - y


Example.add_producer = core.PRODUCERS[0]
Example.add_consumer = core.CONSUMERS[0]
Example.subtract_producer = core.PRODUCERS[1]
Example.subtract_consumer = core.CONSUMERS[1]


def set_producer() -> None:
    os.environ[core.ENV_VARSNAP] = 'true'
    os.environ[core.ENV_ENV] = 'production'
    os.environ[core.ENV_PRODUCER_TOKEN] = 'producer-umakrqit4l021plfg75q'
    os.environ[core.ENV_CONSUMER_TOKEN] = ''


def set_consumer() -> None:
    os.environ[core.ENV_VARSNAP] = 'true'
    os.environ[core.ENV_ENV] = 'development'
    os.environ[core.ENV_PRODUCER_TOKEN] = ''
    os.environ[core.ENV_CONSUMER_TOKEN] = 'consumer-tz1ffce4u9lepxjamw6b'


def reset() -> None:
    core.PRODUCERS = []
    core.CONSUMERS = []


def get_trial(uuid: Optional[str] = None) -> Optional[
        Dict[str, Union[bool, str]]]:
    LOGIN_URL = 'https://www.varsnap.com/login_demo/'
    GET_TRIAL_URL = 'https://www.varsnap.com/api/trial/get/'
    with requests.Session() as session:
        session.get(LOGIN_URL)
        response = session.get(GET_TRIAL_URL)
        data = response.json()['data']
        for trial in data:
            if trial['id'] == uuid or not uuid:
                trial_cast = cast(Dict[str, Union[bool, str]], trial)
                return trial_cast
    return None


class TestTest(unittest.TestCase):
    def test_generate_reference_function(self) -> None:
        f = generate_reference_function()
        self.assertEqual(f(2, 3), 6)
        self.assertEqual(f(4, 5), 20)
        self.assertEqual(f(6, 7), 42)

    def test_generate_test_function(self) -> None:
        f = generate_test_function()
        self.assertEqual(f(2, 3), 7)
        self.assertEqual(f(4, 5), 21)
        self.assertEqual(f(6, 7), 43)

    def test_comparison(self) -> None:
        f1 = generate_reference_function()
        f2 = generate_test_function()
        self.assertNotEqual(f1(2, 3), f2(2, 3))
        self.assertNotEqual(f1(4, 5), f2(4, 5))
        self.assertNotEqual(f1(6, 7), f2(6, 7))
        self.assertEqual(core.get_signature(f1), core.get_signature(f2))

    def test_example_class_add(self) -> None:
        e = Example(2)
        total = e.add(3)
        self.assertEqual(total, 5)
        self.assertEqual(e.x, 5)
        self.assertIsNotNone(e.add_producer)
        self.assertIsNotNone(e.add_consumer)

    def test_example_class_subtract(self) -> None:
        result = Example.subtract(3, 2)
        self.assertEqual(result, 1)
        self.assertIsNotNone(Example.subtract_producer)
        self.assertIsNotNone(Example.subtract_consumer)


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        reset()
        self.original_configure_logger = assert_generator._configure_logger
        assert_generator._configure_logger = mock_logger

    def tearDown(self) -> None:
        assert_generator._configure_logger = self.original_configure_logger

    def assert_in_line(self, strings: List[str], content: str) -> None:
        lines = content.split("\n")
        for snippet in strings:
            lines = [c for c in lines if snippet in c]
        self.assertTrue(
            len(lines) > 0,
            '"%s" is not in "%s"' % (str(strings), content)
        )

    def test_produce_consume(self) -> None:
        f = core.varsnap(generate_reference_function())
        set_producer()
        f(2, 3)
        f(4, 5)
        f(6, 7)
        set_consumer()
        all_matches, all_logs = assert_generator.test()
        self.assertTrue(all_matches)
        self.assertEqual(all_logs, '')
        trial = get_trial()
        assert trial
        self.assertTrue(trial['matches'])

    def test_produce_consume_fail(self) -> None:
        f = core.varsnap(generate_reference_function())
        set_producer()
        f(2, 3)
        f(4, 5)
        f(6, 7)
        reset()
        set_consumer()
        f = core.varsnap(generate_test_function())
        all_matches, all_logs = assert_generator.test()
        self.assertFalse(all_matches)
        self.assert_in_line(['Report URL', 'www.varsnap.com'], all_logs)
        self.assert_in_line(['Function:', 'example'], all_logs)
        self.assert_in_line(['Function input args:', '(2, 3)'], all_logs)
        self.assert_in_line(['kwargs', '{}'], all_logs)
        self.assert_in_line(['Production function outputs', '6'], all_logs)
        self.assert_in_line(['Your function outputs', '7'], all_logs)
        self.assert_in_line(['Matching outputs:', 'False'], all_logs)
        trial = get_trial()
        assert trial
        self.assertFalse(trial['matches'])

    def test_produce_consume_example_add(self) -> None:
        set_producer()
        assert Example.add_producer is not None
        assert Example.add_consumer is not None
        core.PRODUCERS = [Example.add_producer]
        core.CONSUMERS = [Example.add_consumer]
        e = Example(4)
        e.add(5)
        reset()

        core.PRODUCERS = [Example.add_producer]
        core.CONSUMERS = [Example.add_consumer]
        set_consumer()
        all_matches, all_logs = assert_generator.test()
        self.assertTrue(all_matches, all_logs)
        self.assertEqual(all_logs, '')
        trial = get_trial()
        assert trial
        self.assertTrue(trial['matches'])

    def test_produce_consume_example_subtract(self) -> None:
        set_producer()
        assert Example.subtract_producer is not None
        assert Example.subtract_consumer is not None
        core.PRODUCERS = [Example.subtract_producer]
        core.CONSUMERS = [Example.subtract_consumer]
        Example.subtract(3, 2)
        reset()

        core.PRODUCERS = [Example.subtract_producer]
        core.CONSUMERS = [Example.subtract_consumer]
        set_consumer()
        all_matches, all_logs = assert_generator.test()
        self.assertTrue(all_matches, all_logs)
        self.assertEqual(all_logs, '')
        trial = get_trial()
        assert trial
        self.assertTrue(trial['matches'])
