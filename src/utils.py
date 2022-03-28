import json
import secrets
import string
import typing
from datetime import datetime

import aiofiles

from config import ADMIN_IDS

def generate_referral_code(length: int = 5) -> str:
    """Generates a referral code"""
    return "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(length))

def get_datetime_now() -> int:
    return int(datetime.timestamp(datetime.now()))

def is_there_user(user_id: int, ref_user: typing.Dict) -> bool:
    """Does the referral have this user"""
    for ref in ref_user:
        if ref["user_id"] == user_id:
            return True
    else:
        return False

async def get_chat_id_in_file() -> typing.List:
    async with aiofiles.open(ADMIN_IDS, "r", encoding="utf-8") as file:
        data: typing.List[typing.Dict] = json.loads(await file.read())
    chat_ids = []
    for d in data:
        chat_ids.append(d["chat_id"])
    return chat_ids