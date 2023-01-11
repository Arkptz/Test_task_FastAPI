import aiohttp


async def logs(cont, name):
    conn = get_connect()
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(f"http://xx/containers/{cont}/logs?follow=1&stdout=1") as resp:
            async for line in resp.content:
                print(name, line)

def get_connect():
    return aiohttp.UnixConnector(path="/var/run/docker.sock")