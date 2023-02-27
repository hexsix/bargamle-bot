"""
author: hexsix
date: 2023/02/27
description: upload png to p.sda1.dev
"""

import httpx
import json
import logging

from configs import configs


logger = logging.getLogger('psda1dev_utils')


async def upload_images(filename: str):
    async with httpx.AsyncClient(proxies=configs.proxies) as client:
        files = {'file': open(filename, 'rb')}
        for _ in range(3):
            try:
                r = await client.post('https://p.sda1.dev/api/v1/upload_external', files=files)
                if not r.is_success:
                    logger.error(f'/upload failed: filename: {filename}, response: {r}, response text: {r.text}')
                    continue
                else:
                    text_json = json.loads(r.text)
                    if text_json['success']:
                        logger.info(f'/upload success: filename: {filename}, response: {r}, response text: {r.text}')
                        return text_json['data']
                    else:
                        logger.error(f'/upload failed: filename: {filename}, response: {r}, response text: {r.text}')
                        continue
            except Exception as e:
                logger.error(f'/upload failed: filename: {filename}, exception: {e}')
                continue
        return {}


if __name__ == '__main__':
    import asyncio
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    print(asyncio.run(upload_images('sample.jpeg')))
