import json
import smtplib

from email.mime.text import MIMEText

import aiohttp
import aio_pika

from src.utils import get_chat_id_in_file
from config import TB_TOKEN, RABBIT_MQ_URL, QUEUE, SENDER_PASSWORD, SENDER_EMAIL, logger

async def send_to_bot(message: str):
    """
    Send a message to the telegram bot
    :param message: Message text
    :return: The status of the completed work
    """
    try:
        async with aiohttp.ClientSession() as session:
            for user_id in await get_chat_id_in_file():
                # Send a request to the bot.
                async with session.get(
                    f"https://api.telegram.org/bot{TB_TOKEN}/sendMessage",
                    params={
                        # You can get it from @username_to_id_bot.
                        "chat_id": user_id,
                        "text": message,
                        # So that you can customize the text.
                        "parse_mode": "html"
                    }
                ) as response:
                    if not response.ok:
                        logger.error(f'MESSAGE WAS NOT SENT: {message}. {await response.text()}')
                    else:
                        logger.error(f'MESSAGE HAS BEEN SENT: {message}.')

    except Exception as error:
        raise error

async def send_to_rabbit_mq(message: json):
    connection = None
    try:
        connection = await aio_pika.connect_robust(
            url=RABBIT_MQ_URL,
        )
        channel = aio_pika.Channel = await connection.channel()
        await channel.declare_queue(QUEUE)
        await channel.default_exchange.publish(
            message=aio_pika.Message(body=f"{message}".encode()),
            routing_key=QUEUE
        )
        logger.error(f'MESSAGE HAS BEEN SENT: {message}.')
    except Exception as error:
        raise error
    finally:
        if connection is not None:
            await connection.close()

def send_to_email(message: str, email: str, subject: str):
    connection = None
    try:
        connection = smtplib.SMTP(email, 587)
        connection.starttls()

        connection.login(SENDER_EMAIL, SENDER_PASSWORD)
        message = MIMEText(message)
        message["Subject"] = subject
        connection.sendmail(SENDER_EMAIL, SENDER_EMAIL, message.as_string())

        logger.error(f'MESSAGE HAS BEEN SENT: {message}.')
    except Exception as error:
        raise error
    finally:
        if connection is not None:
            connection.close()