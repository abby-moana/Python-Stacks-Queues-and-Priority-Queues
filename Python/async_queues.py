import argparse
import asyncio
from collections import Counter

import aiohttp


async def main(args):
    session = aiohttp.ClientSession()
    try:
        links = Counter()
    finally:
        await session.close()