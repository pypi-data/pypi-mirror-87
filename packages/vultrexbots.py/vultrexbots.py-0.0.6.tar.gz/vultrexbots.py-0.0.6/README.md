# vultrexbots.py
##### **DISCLAIMER!** This is an unofficial package!

Install:
``
pip install vultrexbots.py
``

```py
import vultrexbots

vbk = "apikey"

cli = vultrexbots.Client(botId=642728778535141376, apiKey=vbk)

out = cli.get_bot_info()

reviews = cli.get_bot_reviews()

print(reviews.review) # change review to any needed info

# cli.post_bot_count(serverCount=42, shardCount=0)

print(out.github) # replace github with any other params
```