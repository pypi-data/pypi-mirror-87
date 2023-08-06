# Third party test lib
import threading
from contextlib import contextmanager
from os import environ

import pytest
from consul_sdk import ConsulLock, UnableToAcquireLock, ConsulClient

import time

from uuid import uuid4


@pytest.fixture
def client():
    yield ConsulClient(url=environ.get("CONSUL_ADDR"))


@pytest.fixture
def other_client():
    yield ConsulClient(url=environ.get("CONSUL_ADDR"))


def _lock_fn(client):
    @contextmanager
    def f(lock_key):
        consul_lock = ConsulLock(client, lock_key=lock_key)
        with consul_lock:
            yield

    return f


@pytest.fixture
def lock_fn(client):
    return _lock_fn(client)


@pytest.fixture
def other_lock_fn(other_client):
    return _lock_fn(other_client)


def acquire_lock_and_sleep(key, lock_fn):
    with lock_fn(key):
        time.sleep(2)


@pytest.mark.integration
def test_consul_locking_different_instances(lock_fn, other_lock_fn):
    key = str(uuid4())
    other_key = str(uuid4())
    t1 = threading.Thread(target=acquire_lock_and_sleep, args=(key, other_lock_fn))
    t1.start()

    with pytest.raises(UnableToAcquireLock):
        with lock_fn(key):
            pass

    with lock_fn(other_key):
        pass


@pytest.mark.integration
def test_lock_reraises_exact_same_exception(lock_fn):
    key = str(uuid4())

    class MyException(Exception):
        pass

    with pytest.raises(MyException) as exc1:
        raise MyException("oops")

    with pytest.raises(MyException) as exc2:
        with lock_fn(key):
            raise MyException("oops")

    assert exc1.type == exc2.type
    assert str(exc1.value) == str(exc2.value)
