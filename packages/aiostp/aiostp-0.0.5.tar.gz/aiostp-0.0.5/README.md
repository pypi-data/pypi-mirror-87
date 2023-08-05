asyncio client library for stpmex.com
# STP – Async python client library for stpmex.com

[![test](https://github.com/cuenca-mx/aiostp/workflows/test/badge.svg)](https://github.com/cuenca-mx/aiostp/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/aiostp/branch/main/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/aiostp)
![release](https://github.com/cuenca-mx/aiostp/workflows/release/badge.svg)


# Installation

`pip install aiostp`

# Authentication

The preferred way to configure the credentials for the client is to set the
`STP_PRIVATE_LOCATION` and `STP_KEY_PASSPHRASE` environment variables. The client
library will automatically configure based on the values of those variables.
`STP_PRIVATE_LOCATION` can be the route to the file, or the private key itself.

To configure manually:
```python
import aiostp

aiostp.configure(priv_key='PKxxxx', priv_key_passphrase='yyyyyy')
```
