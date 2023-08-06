import time
from os import environ

import pytest

from consul_sdk.client import ConsulClient


@pytest.fixture
def client():
    yield ConsulClient(url=environ.get("CONSUL_ADDR"))


@pytest.mark.integration
def test_create_and_get_session(client):
    session_id = client.create_session(30)
    assert session_id == client.get_session(session_id)


@pytest.mark.integration
def test_renew_session(client):
    session_id = client.create_session(10)
    assert session_id == client.get_session(session_id)

    time.sleep(9)
    client.renew_session(session_id)

    time.sleep(2)
    assert client.get_session(session_id) is not None


@pytest.mark.skip("Failing")
def test_get_session_returns_none_if_session_expired(client):
    session_id = client.create_session(10)
    assert session_id == client.get_session(session_id)

    time.sleep(15)
    assert client.get_session(session_id) is None


@pytest.mark.integration
def test_acquire_and_release_lock(client):
    session_id = client.create_session(10)

    assert client.acquire_lock("my-key", session_id)
    assert client.release_lock("my-key", session_id)


@pytest.mark.integration
def test_acquire_and_release_txn_locks(client):
    session_id = client.create_session(10)

    assert client.acquire_locks(["my-key-1", "my-key-2", "my-key-3"], session_id)
    assert client.release_locks(["my-key-1", "my-key-2", "my-key-3"], session_id)


@pytest.mark.integration
def test_acquire_and_reacquire_same_txn_locks_raises_error(client):
    session_id_1 = client.create_session(10)
    session_id_2 = client.create_session(10)

    assert client.acquire_locks(["my-key-1", "my-key-2"], session_id_1)
    assert not client.acquire_locks(["my-key-1"], session_id_2)

    assert client.release_locks(["my-key-1", "my-key-2"], session_id_1)

    assert client.acquire_locks(["my-key-1"], session_id_2)
    assert client.release_locks(["my-key-1"], session_id_2)


@pytest.mark.integration
def test_legacy_lock_works_with_new_txn_locks(client):
    session_id_1 = client.create_session(10)
    session_id_2 = client.create_session(10)

    assert client.acquire_lock("my-key-1", session_id_1)
    assert client.release_locks(["my-key-1"], session_id_1)

    assert client.acquire_lock("my-key-1", session_id_2)
    assert not client.acquire_locks(["my-key-1"], session_id_1)
    assert client.release_lock("my-key-1", session_id_2)

    assert client.acquire_locks(["my-key-1", "my-key-2"], session_id_1)
    assert not client.acquire_lock("my-key-1", session_id_2)
    assert client.release_lock("my-key-1", session_id_1)
    assert client.release_lock("my-key-2", session_id_1)
