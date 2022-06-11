from __future__ import annotations

import asyncio

import pytest

from coredis.cache import ClusterInvalidatingCache, InvalidatingCache
from tests.conftest import targets


@pytest.mark.asyncio
@targets("redis_basic", "redis_basic_raw", "redis_basic_resp3", "redis_basic_raw_resp3")
class TestInvalidatingCache:
    async def test_single_entry_cache(self, client, cloner, _s):
        await client.flushall()
        cache = InvalidatingCache(max_keys=1)
        cached = await cloner(client, cache=cache)
        assert not await cached.get("fubar")
        await client.set("fubar", 1)
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("1")
        await client.incr("fubar")
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("2")

    async def test_eviction(self, client, cloner, _s):
        cache = InvalidatingCache(max_keys=1)
        cached = await cloner(client, cache=cache)
        assert not await cached.get("fubar")
        assert not await cached.get("barbar")
        assert not await cached.get("fubar")
        assert not await cached.get("barbar")
        await client.set("fubar", 1)
        await client.set("barbar", 2)
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("1")
        assert await cached.get("barbar") == _s("2")
        await client.pexpire("fubar", 1)
        await client.pexpire("barbar", 1)
        await asyncio.sleep(0.2)
        assert not await cached.get("fubar")
        assert not await cached.get("barbar")

    async def test_single_entry_cache_tracker_disconnected(self, client, cloner, _s):
        cache = InvalidatingCache(max_keys=1)
        cached = await cloner(client, cache=cache)
        assert not await client.get("fubar")
        await client.set("fubar", 1)
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("1")
        await client.incr("fubar")
        cache.connection.disconnect()
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("2")


@pytest.mark.asyncio
@targets(
    "redis_cluster",
    "redis_cluster_raw",
    "redis_cluster_resp3",
    "redis_cluster_raw_resp3",
)
class TestClusterInvalidatingCache:
    async def test_single_entry_cache(self, client, cloner, _s):
        await client.flushall()
        cache = ClusterInvalidatingCache(max_keys=1)
        cached = await cloner(client, cache=cache)
        assert not await cached.get("fubar")
        await client.set("fubar", 1)
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("1")
        await client.incr("fubar")
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("2")

    async def test_eviction(self, client, cloner, _s):
        cache = ClusterInvalidatingCache(max_keys=1)
        cached = await cloner(client, cache=cache)
        assert not await cached.get("fubar")
        assert not await cached.get("barbar")
        assert not await cached.get("fubar")
        assert not await cached.get("barbar")
        await client.set("fubar", 1)
        await client.set("barbar", 2)
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("1")
        assert await cached.get("barbar") == _s("2")
        await client.pexpire("fubar", 1)
        await client.pexpire("barbar", 1)
        await asyncio.sleep(0.2)
        assert not await cached.get("fubar")
        assert not await cached.get("barbar")

    async def test_single_entry_cache_tracker_disconnected(self, client, cloner, _s):
        cache = ClusterInvalidatingCache(max_keys=1)
        cached = await cloner(client, cache=cache)
        assert not await client.get("fubar")
        await client.set("fubar", 1)
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("1")
        await client.incr("fubar")
        [ncache.connection.disconnect() for ncache in cache.node_caches.values()]
        await asyncio.sleep(0.2)
        assert await cached.get("fubar") == _s("2")
