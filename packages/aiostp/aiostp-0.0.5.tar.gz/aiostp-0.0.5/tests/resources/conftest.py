import asyncio

import aiostp

loop = asyncio.get_event_loop()

loop.run_until_complete(aiostp.configure(demo=True))
