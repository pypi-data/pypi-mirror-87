from typing import List, Dict
from http import HTTPStatus

import requests


class ConsulClient:
    def __init__(self, url="http://127.0.0.1:8500", service_name=None):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{url}"

        self._url = url
        self._service_name = service_name

    def acquire_lock(self, key, session_id):
        payload = {"acquire": session_id}
        return self._put_key(key, payload)

    def release_lock(self, key, session_id):
        payload = {"release": session_id}
        return self._put_key(key, payload)

    def acquire_locks(self, keys: List[str], session_id):
        payload = self._lock_payload(type="lock", keys=keys, session_id=session_id)
        return self._run_in_txn(payload)

    def release_locks(self, keys: List[str], session_id):
        payload = self._lock_payload(type="unlock", keys=keys, session_id=session_id)
        return self._run_in_txn(payload)

    def get_key(self, key):
        response = requests.get(f"{self._url}/v1/kv/{key}")

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        self._assert_response(response)
        return response.json()[0]

    def create_session(
        self, ttl_in_secs: int, lock_delay_in_secs: int = 15, behavior="release"
    ):
        payload = {
            "LockDelay": f"{lock_delay_in_secs}s",
            "Name": self._service_name,
            "Node": None,
            "Checks": [],
            "Behavior": behavior,
            "TTL": f"{ttl_in_secs}s",
        }

        response = requests.put(f"{self._url}/v1/session/create", json=payload)
        self._assert_response(response)

        return response.json()["ID"]

    def renew_session(self, session_id):
        response = requests.put(f"{self._url}/v1/session/renew/{session_id}")
        self._assert_response(response)

    def get_session(self, session_id):
        response = requests.get(f"{self._url}/v1/session/info/{session_id}")
        self._assert_response(response)

        data = response.json()
        if len(data) == 0:
            return None

        session = data[0]
        return session["ID"]

    def _lock_payload(self, type: str, keys: List[str], session_id: str):
        return [
            {"KV": {"Verb": type, "Key": key, "Value": None, "Session": session_id}}
            for key in keys
        ]

    def _put_key(self, key, payload):
        response = requests.put(f"{self._url}/v1/kv/{key}", params=payload)
        self._assert_response(response)

        return response.json()

    def _run_in_txn(self, payload: List[Dict]):
        response = requests.put(f"{self._url}/v1/txn", json=payload)
        if response.status_code == HTTPStatus.CONFLICT:
            return False

        self._assert_response(response)
        return response.json()

    def _assert_response(self, response):
        if response.status_code != HTTPStatus.OK:
            raise RuntimeError(
                f"""
                Consul request failed.

                Status code: {response.status_code}
                Body:

                {response.text}
            """
            )
