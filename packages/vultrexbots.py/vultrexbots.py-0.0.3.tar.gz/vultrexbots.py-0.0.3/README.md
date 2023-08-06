# vultrexbots.py
##### **DISCLAIMER!** This is an unofficial package!

Install:
``
pip install vultrexbots.py
``

```py
import vultrexbots

cli = vultrexbots.Client()

vbk = "APIKEYHERE"

out = cli.get_bot_info(botId=str(642728778535141376), apiKey=vbk)

print(out.json) # Change 'json' to anything needed (ex: github)
```