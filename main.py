__version__ = '0.02'

import asyncio
import os
import re

import httpx
import telegram
from dotenv import load_dotenv


load_dotenv('vars.env')


async def send_telegram_message():
    bot = telegram.Bot(telegram_bot_token)
    async with bot:
        await bot.send_message(text=text_to_send, chat_id=os.environ.get('CHAT_ID'))


telegram_bot_token = os.environ.get('TOKEN')

url = 'https://baumguitars.com/2023/10/28/waiting-for-a-baum-check-here/'

regex = r'(?<=<div class=\"circle-val\"><span class=\"circle-counter__number\" data-to-value=\")(.*?)(?=\" data-delimiter=\",\">0<\/span><span class=\"circle-counter__suffix\">%)'

if __name__ == '__main__':
    content = httpx.get(url)
    test_str = content.content.decode('utf-8')
    matches = re.findall(regex, test_str, re.MULTILINE)

    nidhogg_status = matches[8:12]
    nidhogg_status = [int(i) for i in nidhogg_status]
    nidhogg_status = [f'{i}%' if i < 100 else '👍' for i in nidhogg_status]

    production, shipping_dk, qc_setup, shipping_me = nidhogg_status

    text_to_send = f"""🎸 NIDHOGG STATUS 🎸\nProduction: {production}\nShipping to DK: {shipping_dk}\nQC and Setup: {qc_setup}\nShipping to You: {shipping_me} """

    asyncio.run(send_telegram_message())
