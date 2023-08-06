# Run consul agent consul agent -dev to run this file.
import time
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from consul_sdk.consul_lock import ConsulLock, UnableToAcquireLock


@pytest.fixture
def consul_client():
    return MagicMock()


def test_consul_lock_creates_a_session_if_doesnt_exist(consul_client):
    consul_client.get_session = MagicMock(return_value=None)
    consul_client.create_session = MagicMock(return_value=str(uuid4()))

    with ConsulLock(client=consul_client, lock_key="my-key"):
        pass
    assert consul_client.create_session.called


def test_consul_lock_renews_a_session_if_time_left_to_expire_is_less_than_half_ttl(
    consul_client,
):
    session_id = str(uuid4())
    consul_client.get_session = MagicMock(return_value=None)
    consul_client.create_session = MagicMock(return_value=session_id)
    consul_client.renew_session = MagicMock(return_value=None)

    with ConsulLock(client=consul_client, lock_key="my-key", ttl=4):
        pass
    time.sleep(2)

    consul_client.get_session = MagicMock(return_value=session_id)
    with ConsulLock(client=consul_client, lock_key="my-key", ttl=4):
        pass

    assert consul_client.renew_session.called


def test_consul_lock_doesnt_renew_a_session_if_time_left_to_renew_is_gt_half_ttl(
    consul_client,
):
    session_id = str(uuid4())
    consul_client.get_session = MagicMock(return_value=None)
    consul_client.create_session = MagicMock(return_value=session_id)

    with ConsulLock(client=consul_client, lock_key="my-key", ttl=2):
        pass

    consul_client.get_session = MagicMock(return_value=session_id)
    with ConsulLock(client=consul_client, lock_key="my-key", ttl=2):
        pass

    assert not consul_client.renew_session.called


def test_consul_lock_takes_lock_before_starting_the_process(consul_client):
    session_id = str(uuid4())
    consul_client.get_session = MagicMock(return_value=None)
    consul_client.create_session = MagicMock(return_value=session_id)

    with ConsulLock(client=consul_client, lock_key="my-key", ttl=2):
        pass

    assert consul_client.acquire_locks.called
    assert consul_client.acquire_locks.call_args[1]["keys"] == ["my-key"]


def test_consul_lock_releases_lock_on_successful_exit(consul_client):
    session_id = str(uuid4())
    consul_client.get_session = MagicMock(return_value=None)
    consul_client.create_session = MagicMock(return_value=session_id)

    with ConsulLock(client=consul_client, lock_key="my-key", ttl=2):
        pass

    assert consul_client.release_locks.called
    assert consul_client.release_locks.call_args[1]["keys"] == ["my-key"]


def test_consul_lock_releases_lock_on_successful_exit_for_multi_locks(consul_client):
    session_id = str(uuid4())
    consul_client.get_session = MagicMock(return_value=None)
    consul_client.create_session = MagicMock(return_value=session_id)

    with ConsulLock(consul_client, "my-key-1", "my-key-2", ttl=2):
        pass

    assert consul_client.release_locks.called
    assert consul_client.release_locks.call_args[1]["keys"] == ["my-key-1", "my-key-2"]


def test_consul_lock_releases_lock_if_process_raises_exception(consul_client):
    session_id = str(uuid4())
    consul_client.get_session = MagicMock(return_value=None)
    consul_client.create_session = MagicMock(return_value=session_id)

    with pytest.raises(Exception):
        with ConsulLock(client=consul_client, lock_key="my-key", ttl=2):
            raise Exception("FIRE")

    assert consul_client.release_locks.called
    assert consul_client.release_locks.call_args[1]["keys"] == ["my-key"]


def test_consul_lock_raises_unable_to_acquire_locks_if_already_taken(consul_client):
    session_id = str(uuid4())
    consul_client.get_session = MagicMock(return_value=None)
    consul_client.create_session = MagicMock(return_value=session_id)
    consul_client.acquire_locks = MagicMock(return_value=False)

    with pytest.raises(UnableToAcquireLock):
        with ConsulLock(client=consul_client, lock_key="my-key", ttl=5):
            pass


def test_consul_lock_raises_unable_to_acquire_locks_if_already_taken_for_multi_locks(
    consul_client,
):
    session_id = str(uuid4())
    consul_client.get_session = MagicMock(return_value=None)
    consul_client.create_session = MagicMock(return_value=session_id)
    consul_client.acquire_locks = MagicMock(return_value=False)

    with pytest.raises(UnableToAcquireLock):
        with ConsulLock(consul_client, "my-key-1", "my-key-2", ttl=5):
            pass
