import ujson as json
import requests

from .lib.util import objects, exceptions


class Client:
    def __init__(self):
        self.api = "https://api.discordbots.co/v1"

    def get_bot_info(self, botId: int, apiKey: str):
        headers = {
            "Authorization": apiKey
        }
        response = requests.get(f"{self.api}/public/bot/{botId}", headers=headers)
        if response.status_code != 200: raise exceptions.CheckException(json.loads(response.text))
        else: return objects.botInfo(json.loads(response.text)["response"])

    def post_bot_count(self, botId: int, apiKey: str, serverCount: int, shardCount: int):
        headers = {
            "Authorization": apiKey,
            "Content-Type": 'application/json'
        }
        payLoad = {
            "serverCount": int(serverCount),
            "shardCount": int(shardCount)
        }
        response = requests.post(f"{self.api}/public/bot/{botId}/stats", headers=headers, json=payLoad)
        if response.status_code != 200: raise exceptions.CheckException(json.loads(response.text))
        else:
            return print("[vultrexbots.py] Shard/Guild posting success, please wait 5 minutes or you would be ratelimited!")