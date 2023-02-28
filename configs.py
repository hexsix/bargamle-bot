"""
author: hexsix
date: 2023/02/27
description: configs
"""

import json
import os


class Configs(object):
    def __init__(self):
        if os.path.exists('.env'):  # self-host
            from dotenv import load_dotenv
            load_dotenv()
        self.chat_id = int(os.environ['CHAT_ID'])
        self.tg_token = os.environ['TG_TOKEN']
        self.use_proxies = bool(os.environ['USE_PROXIES'])
        if self.use_proxies:
            self.proxies = json.loads(os.environ['PROXIES'])
        else:
            self.proxies = {}
    
    def __str__(self):
        return f"telegram token: ******\n" \
               f"telegram chat id: {self.chat_id}\n" \
               f"use proxies: {self.use_proxies}\n" \
               f"proxies: {json.dumps(self.proxies)}"


configs = Configs()


if __name__ == '__main__':
    print(configs)
