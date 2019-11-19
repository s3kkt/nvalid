from aiohttp import ClientSession


async def send_message(text, *, channel="", url="", color=""):
    content = {
        "channel": str(channel),
        "username": "n-validator",
        "icon_emoji": ":nginx:",
        "blocks": [{"type": "divider"}],
        "attachments": [{
            "fallback": "Nginx config test failed!",
            "text": text,
            "color": color
        }]
    }

    async with ClientSession() as s:
        async with s.post(url, json=content) as response:
            if response.status != 200:
                print(url)
                print(response.status)
                print("Failed to send message")
                print(content)
                print((await response.content.read()).decode())
                return False
            return True
