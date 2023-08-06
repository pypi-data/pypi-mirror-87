# Consul SDK

Consul library to use locks on consul.

### Basic Usage

    In [1]: from consul_sdk import ConsulClient, ConsulLock, UnableToAcquireLock

    In [2]: client = ConsulClient(node_name=None, service_name=None, token="abc")

    In [3]: client
    Out[3]: <consul_sdk.client.ConsulClient at 0x10206add8>

    In [4]: with ConsulLock(client, "my-key"):
       ...:     import time
       ...:     print("Hi")
       ...:     time.sleep(5)
       ...:     print("Bye")
       ...:
    Hi
    Bye

### Releasing

- `make bump_version`
- Update [the Changelog]
- Commit changes to `Changelog`, `setup.py` and `setup.cfg`.
- `make push_tag` (this'll push a tag that will trigger python package checks)
- `make release` (this will release the tag)

- You can do `make push_tag_and_release` to combine the above two steps
