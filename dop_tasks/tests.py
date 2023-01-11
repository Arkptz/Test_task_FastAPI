from unittest import IsolatedAsyncioTestCase
import asyncio
import unittest
from part import logs, get_connect


class Test(IsolatedAsyncioTestCase):

    async def test_connect(self):
        res = get_connect()

    async def test_functionality(self):
        result = await logs('test', 'test')


if __name__ == "__main__":
    unittest.main()