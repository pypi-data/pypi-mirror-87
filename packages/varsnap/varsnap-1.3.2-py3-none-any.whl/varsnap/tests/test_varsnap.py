import json
import logging
import os
import sys
import time
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from typing import Any, Iterator

from varsnap import core
from varsnap.__version__ import __version__


logger = logging.getLogger(core.__name__)
logger.disabled = True


class EnvVar(unittest.TestCase):
    def setUp(self) -> None:
        self.orig_varsnap = os.environ.get(core.ENV_VARSNAP, '')
        self.orig_env = os.environ.get(core.ENV_ENV, '')
        self.orig_producer_token = os.environ.get(core.ENV_PRODUCER_TOKEN, '')
        self.orig_consumer_token = os.environ.get(core.ENV_CONSUMER_TOKEN, '')
        core.CONSUMERS = []
        core.PRODUCERS = []

    def tearDown(self) -> None:
        os.environ[core.ENV_VARSNAP] = self.orig_varsnap
        os.environ[core.ENV_ENV] = self.orig_env
        os.environ[core.ENV_PRODUCER_TOKEN] = self.orig_producer_token
        os.environ[core.ENV_CONSUMER_TOKEN] = self.orig_consumer_token


class TestEnvVar(EnvVar):
    def test_env_var(self) -> None:
        os.environ[core.ENV_VARSNAP] = 'true'
        env = core.env_var(core.ENV_VARSNAP)
        self.assertEqual(env, 'true')

    def test_downcases_env_var(self) -> None:
        os.environ[core.ENV_VARSNAP] = 'TRUE'
        env = core.env_var(core.ENV_VARSNAP)
        self.assertEqual(env, 'true')

    def test_unset_var(self) -> None:
        del os.environ[core.ENV_VARSNAP]
        env = core.env_var(core.ENV_VARSNAP)
        self.assertEqual(env, '')


class TestEqual(EnvVar):
    def test_primitives(self) -> None:
        self.assertTrue(core.equal(1, 1))
        self.assertFalse(core.equal(1, '1'))
        self.assertTrue(core.equal('asdf', 'asdf'))

    def test_iterables(self) -> None:
        self.assertTrue(core.equal([1, 2, 3], [1, 2, 3]))
        self.assertTrue(core.equal({1: 'a', 2: 'b'}, {1: 'a', 2: 'b'}))
        self.assertFalse(core.equal([1, 2], [1, 2, 3]))
        self.assertFalse(core.equal([1, 2, 3], [1, 2, 4]))
        self.assertFalse(core.equal({1: 2}, {}))
        self.assertFalse(core.equal({1: 2}, {1: 3}))
        self.assertFalse(core.equal({1: 2}, {2: 2}))

    def test_objects(self) -> None:
        class X():
            def __init__(self, x: Any) -> None:
                self.x = x
        self.assertTrue(core.equal(X('asdf'), X('asdf')))
        self.assertFalse(core.equal(X('asdf'), X('qwer')))
        self.assertTrue(core.equal(X(X('asdf')), X(X('asdf'))))


class TestGetSignature(unittest.TestCase):
    def assertEqualVersion(self, signature: str, expected: str) -> None:
        self.assertEqual(signature, expected % __version__)

    def test_standalone_func(self) -> None:
        signature = core.get_signature(core.env_var)
        self.assertEqualVersion(signature, 'python.%s.env_var')

    def test_class_func(self) -> None:
        signature = core.get_signature(core.Producer.serialize)
        self.assertEqualVersion(signature, 'python.%s.Producer.serialize')

    def test_instance_func(self) -> None:
        signature = core.get_signature(core.Producer.__init__)
        self.assertEqualVersion(signature, 'python.%s.Producer.__init__')


class TestLimitString(unittest.TestCase):
    def test_small_string(self) -> None:
        x = 'asdf'
        self.assertEqual(core.limit_string(x), x)

    def test_medium_string(self) -> None:
        x = 'x' * 30
        self.assertEqual(core.limit_string(x), x)

    def test_long_string(self) -> None:
        x = 'x' * 50
        limited = core.limit_string(x)
        self.assertEqual(limited[:27], 'x' * 27)
        self.assertEqual(limited[27:], '...')


class TestProducer(EnvVar):
    def setUp(self) -> None:
        super(TestProducer, self).setUp()
        os.environ[core.ENV_VARSNAP] = 'true'
        os.environ[core.ENV_ENV] = 'production'
        os.environ[core.ENV_PRODUCER_TOKEN] = 'asdf'

        self.producer = core.Producer(core.env_var)

    def test_init(self) -> None:
        target_func = MagicMock()
        producer = core.Producer(target_func)
        self.assertEqual(producer.target_func, target_func)
        self.assertIn(producer, core.PRODUCERS)

    def test_is_enabled(self) -> None:
        self.assertTrue(core.Producer.is_enabled())

        os.environ[core.ENV_VARSNAP] = 'false'
        self.assertFalse(core.Producer.is_enabled())
        os.environ[core.ENV_VARSNAP] = 'true'

        os.environ[core.ENV_ENV] = 'development'
        self.assertFalse(core.Producer.is_enabled())
        os.environ[core.ENV_ENV] = 'production'

        os.environ[core.ENV_PRODUCER_TOKEN] = ''
        self.assertFalse(core.Producer.is_enabled())
        os.environ[core.ENV_PRODUCER_TOKEN] = 'asdf'

    def test_serialize(self) -> None:
        data = core.Producer.serialize('abcd')
        self.assertGreater(len(data), 0)

    def test_serialize_known_error(self) -> None:
        def f(n: int) -> Iterator[int]:
            yield n
        with self.assertRaises(core.SerializeError):
            core.Producer.serialize(f(2))

    @patch('varsnap.core.pickle.dumps')
    def test_serialize_unknown_error(self, mock_dumps: MagicMock) -> None:
        mock_dumps.side_effect = MemoryError()
        with self.assertRaises(MemoryError):
            core.Producer.serialize('asdf')

    @patch('requests.post')
    def test_produce_not_enabled(self, mock_post: MagicMock) -> None:
        os.environ[core.ENV_VARSNAP] = 'false'
        self.producer.produce(['a'], {'b': 'c'}, 'c')
        self.assertFalse(mock_post.called)

    @patch('requests.post')
    def test_produce(self, mock_post: MagicMock) -> None:
        self.producer.produce(['a'], {'b': 'c'}, 'c')
        self.assertEqual(mock_post.call_args[0][0], core.PRODUCE_SNAP_URL)
        data = mock_post.call_args[1]['data']
        self.assertEqual(data['producer_token'], 'asdf')
        self.assertEqual(data['signature'], core.get_signature(core.env_var))
        self.assertIn('inputs', data)
        self.assertIn('prod_outputs', data)


class TestConsumer(EnvVar):
    def setUp(self) -> None:
        super(TestConsumer, self).setUp()
        os.environ[core.ENV_VARSNAP] = 'true'
        os.environ[core.ENV_ENV] = 'development'
        os.environ[core.ENV_CONSUMER_TOKEN] = 'asdf'

        self.target_func = MagicMock()
        self.consumer = core.Consumer(self.target_func)

    def test_init(self) -> None:
        target_func = MagicMock()
        consumer = core.Consumer(target_func)
        self.assertEqual(consumer.target_func, target_func)
        self.assertIn(consumer, core.CONSUMERS)

    def test_is_enabled(self) -> None:
        self.assertTrue(core.Consumer.is_enabled())

        os.environ[core.ENV_VARSNAP] = 'false'
        self.assertFalse(core.Consumer.is_enabled())
        os.environ[core.ENV_VARSNAP] = 'true'

        os.environ[core.ENV_ENV] = 'production'
        self.assertFalse(core.Consumer.is_enabled())
        os.environ[core.ENV_ENV] = 'development'

        os.environ[core.ENV_CONSUMER_TOKEN] = ''
        self.assertFalse(core.Consumer.is_enabled())
        os.environ[core.ENV_CONSUMER_TOKEN] = 'asdf'

    def test_deserialize(self) -> None:
        data = core.Producer.serialize('abcd')
        output = core.Consumer.deserialize(data)
        self.assertEqual(output, 'abcd')

        data = core.Producer.serialize(EnvVar)
        output = core.Consumer.deserialize(data)
        self.assertEqual(output, EnvVar)

    def test_deserialize_known_error(self) -> None:
        with self.assertRaises(core.DeserializeError):
            core.Consumer.deserialize('abcd')

    @patch('varsnap.core.pickle.loads')
    def test_deserialize_unknown_error(self, mock_loads: MagicMock) -> None:
        mock_loads.side_effect = MemoryError('asdf')
        with self.assertRaises(MemoryError):
            core.Consumer.deserialize('abcd')

    @patch('requests.post')
    def test_consume_not_enabled(self, mock_post: MagicMock) -> None:
        os.environ[core.ENV_VARSNAP] = 'false'
        self.consumer.consume()
        self.assertFalse(mock_post.called)

    @patch('varsnap.core.qualname')
    @patch('requests.post')
    def test_consume_empty(
        self, mock_post: MagicMock, mock_qualname: MagicMock
    ) -> None:
        mock_qualname.return_value = 'magicmock'
        mock_post.return_value = MagicMock(content='')
        self.consumer.consume()
        self.assertFalse(self.target_func.called)

    @patch('varsnap.core.qualname')
    @patch('requests.post')
    def test_consume(
        self, mock_post: MagicMock, mock_qualname: MagicMock
    ) -> None:
        mock_qualname.return_value = 'magicmock'
        inputs = {
            'args': (2,),
            'kwargs': {},
            'globals': {},
        }
        data = {
            'results': [{
                'id': 'abcd',
                'inputs': core.Producer.serialize(inputs),
                'prod_outputs': core.Producer.serialize((4,)),
            }],
            'status': 'ok',
        }
        data_str = json.dumps(data)
        mock_post.return_value = MagicMock(content=data_str)
        self.target_func.return_value = (4,)
        self.consumer.consume()
        self.assertEqual(self.target_func.call_count, 1)
        self.assertEqual(self.target_func.call_args[0][0], 2)
        snap_consume_request = mock_post.mock_calls[0][2]['data']
        self.assertEqual(snap_consume_request['consumer_token'], 'asdf')
        signature = core.get_signature(core.env_var)
        self.assertEqual(snap_consume_request['signature'], signature)
        trial_produce_request = mock_post.mock_calls[1][2]['data']
        self.assertEqual(trial_produce_request['consumer_token'], 'asdf')
        self.assertEqual(trial_produce_request['snap_id'], 'abcd')
        test_outputs = core.Producer.serialize((4,))
        self.assertEqual(trial_produce_request['test_outputs'], test_outputs)
        self.assertEqual(trial_produce_request['matches'], True)

    @patch('varsnap.core.qualname')
    @patch('requests.post')
    def test_consume_catches_exceptions(
        self, mock_post: MagicMock, mock_qualname: MagicMock
    ) -> None:
        mock_qualname.return_value = 'magicmock'
        inputs = {
            'args': (2,),
            'kwargs': {},
            'globals': {},
        }
        error = ValueError('asdf')
        data = {
            'results': [{
                'id': 'abcd',
                'inputs': core.Producer.serialize(inputs),
                'prod_outputs': core.Producer.serialize(error)
            }],
            'status': 'ok',
        }
        data_str = json.dumps(data)
        mock_post.side_effect = [
            MagicMock(content=data_str),
            MagicMock(content=json.dumps({'status': 'ok'})),
        ]
        self.target_func.side_effect = error
        trials = self.consumer.consume()
        self.assertEqual(self.target_func.call_count, 1)
        self.assertEqual(len(trials), 1)
        self.assertTrue(trials[0].matches)


class TestVarsnap(EnvVar):
    @patch('requests.post')
    def test_no_op(self, mock_post: MagicMock) -> None:
        os.environ[core.ENV_VARSNAP] = 'false'
        mock_func = MagicMock()
        mock_func.__name__ = 'mock_func'
        test_func = core.varsnap(mock_func)
        test_func(1)
        self.assertFalse(mock_post.called)

    @patch('varsnap.core.Consumer.consume')
    @patch('varsnap.core.Producer.produce')
    def test_consume(
        self, mock_produce: MagicMock, mock_consume: MagicMock
    ) -> None:
        if sys.version_info.major < 3:
            # TODO remove this
            return
        mock_func = MagicMock()
        mock_func.__name__ = 'mock_func'
        mock_func.return_value = 2
        varsnap_mock_func = core.varsnap(mock_func)
        result = varsnap_mock_func(1)
        self.assertEqual(result, 2)
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(mock_consume.call_count, 0)
        self.assertEqual(mock_produce.call_count, 1)
        self.assertEqual(mock_produce.call_args[0][2], 2)

    @patch('varsnap.core.Consumer.consume')
    @patch('varsnap.core.Producer.produce')
    def test_consume_exception(
        self, mock_produce: MagicMock, mock_consume: MagicMock
    ) -> None:
        if sys.version_info.major < 3:
            # TODO remove this
            return
        mock_func = MagicMock()
        mock_func.__name__ = 'mock_func'
        mock_func.side_effect = ValueError('asdf')
        varsnap_mock_func = core.varsnap(mock_func)
        with self.assertRaises(ValueError):
            varsnap_mock_func(1)
        time.sleep(0.1)  # Make sure mock_produce has enough time to be called
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(mock_consume.call_count, 0)
        self.assertEqual(mock_produce.call_count, 1)
        self.assertEqual(str(mock_produce.call_args[0][2]), 'asdf')

    @patch('varsnap.core.Producer.produce')
    def test_func_name(self, mock_produce: MagicMock) -> None:
        varsnap_func = core.varsnap(core.Producer.serialize)
        self.assertEqual(varsnap_func.__name__, 'serialize')
