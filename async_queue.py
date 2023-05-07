import asyncio
from typing import Optional, Any

class AsyncQueue:
    def __init__(self):
        self._queue = asyncio.Queue()

    async def get(self) -> Optional[Any]:
        item = await self._queue.get()
        if item is None:
            raise asyncio.CancelledError()
        return item

    async def put(self, item):
        await self._queue.put(item)

    async def close(self):
        await self._queue.put(None)
