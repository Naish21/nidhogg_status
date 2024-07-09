__version__ = "0.04"

import asyncio
import os
import re

import httpx
import telegram
from dotenv import load_dotenv

load_dotenv("vars.env")


async def get_bot(token: str):
    bot = telegram.Bot(token)
    async with bot:
        return await bot.get_me()


async def get_info(token: str):
    bot = telegram.Bot(token)
    async with bot:
        updates = (await bot.get_updates())[0]
        return updates


async def send_telegram_message(token: str, chat_id: str, message: str):
    bot = telegram.Bot(token)
    async with bot:
        await bot.send_message(text=message, chat_id=chat_id)


def get_text_to_send(url: str) -> str:
    content = httpx.get(url)
    test_str = content.content.decode("utf-8")
    regex = r'(?<=<div class=\"circle-val\"><span class=\"circle-counter__number\" data-to-value=\")(.*?)(?=\" data-delimiter=\",\">0<\/span><span class=\"circle-counter__suffix\">%)'
    matches = re.findall(regex, test_str, re.MULTILINE)
    nidhogg_status = matches[8:12]
    nidhogg_status = [f"{i}%" if int(i) < 100 else "👍" for i in nidhogg_status]
    production, shipping_dk, qc_setup, shipping_me = nidhogg_status
    return f"""🎸 NIDHOGG STATUS 🎸\n"""\
           f"""Production: {production}\n"""\
           f"""Shipping to DK: {shipping_dk}\n"""\
           f"""QC and Setup: {qc_setup}\n"""\
           f"""Shipping to You: {shipping_me}"""


if __name__ == "__main__":
    text_to_send = get_text_to_send(url=os.environ.get("URL"))
    asyncio.run(
        send_telegram_message(
            token=os.environ.get("TOKEN"),
            chat_id=os.environ.get("CHAT_ID"),
            message=text_to_send,
        ),
    )
