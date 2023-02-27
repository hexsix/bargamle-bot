"""
author: hexsix
date: 2023/02/27
description: redis utils
"""

import logging
import redis.asyncio as redis

from configs import configs


logger = logging.getLogger('redis_utils')


async def redis_set(key: str, value: str):
    r = await redis.from_url(configs.redis_url)
    for i in range(3):
        try:
            ok = await r.set(key, value)
            if ok:
                logger.info(f'/redis_set success: key: {key}, value: {value}, {i + 1}th try')
                await r.close()
                return 0
            logger.iwarning(f'/redis_set failed: key: {key}, value: {value}, {i + 1}th try')
        except Exception as e:
            logger.iwarning(f'/redis_set failed: key: {key}, value: {value}, {i + 1}th try, exception: {e}')
    await r.close()
    return 1


async def redis_get(key: str) -> str:
    r = await redis.from_url(configs.redis_url)
    for i in range(3):
        try:
            value = await r.get(key)
            logger.info(f'/redis_get success: key: {key}, {i + 1}th try, value: {value}')
            await r.close()
            return value
        except Exception as e:
            logger.iwarning(f'/redis_get failed: key: {key}, {i + 1}th try, exception: {e}')
    await r.close()
    return ''


async def redis_ping():
    r = await redis.from_url(configs.redis_url)
    logger.info(f"Ping successful: {await r.ping()}")
    await r.close()


if __name__ == '__main__':
    import asyncio
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    asyncio.run(redis_ping())
