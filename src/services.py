import json
import typing
from datetime import datetime

from src.db import db
from src.sender import send_to_email, send_to_bot, send_to_rabbit_mq
from src.utils import get_datetime_now, is_there_user

async def search_by_ref_code(referrer: str, user_id: int, lvl: int = 1) -> bool:
    """
    This function adds levels to each referral.
    :param referrer: The referral code of the invitee
    :param user_id: New user ID
    :param lvl: Its hierarchy level. Only 4 lvl
    """
    result = await db.get_referrer_by_referral_code(referral=referrer)
    ref_users = json.loads(result["ref_users"])
    for key, value in ref_users.items():
        if is_there_user(ref_user=value, user_id=user_id):
            return True
    if lvl >= 4:
        ref_users["lvl_4"].append({
            "user_id": user_id,
            "time": get_datetime_now()
        })
    else:
        ref_users[f"lvl_{lvl}"].append({
            "user_id": user_id,
            "time": get_datetime_now()
        })
    status = await db.update_referral_lvl_by_user_id(
        user_id=user_id,
        ref_users=json.dumps(ref_users)
    )
    if status is None:
        raise Exception("Not add referral")
    if result["referrer"] is not None:
        return await search_by_ref_code(referrer=result["referrer"], user_id=user_id, lvl=lvl + 1)
    return True

async def get_user_information(user_id: int, username: str) -> typing.Dict:
    """Returns all information about the user"""
    referral_info = await db.get_referral_info_by_user_id(user_id=user_id)
    return {
        "id": user_id,
        "username": username,
        "datetime": datetime.fromtimestamp(int(referral_info["reg_time"]) / 1000),
        "timestamp": referral_info["reg_time"],
        "referral_code": referral_info["referral_code"],
        "referrer": referral_info["referrer"],
        "ref_users": referral_info["ref_users"]
    }

async def send_to(username: str, email: str, referral_code: str, referrer: str = None):
    await send_if_new(username=username, email=email, referral_code=referral_code, referrer=referrer)
    if referrer:
        await if_not_new(referrer=referrer, new_user=username)

async def send_if_new(username: str, email: str, referral_code: str, referrer: str = None) -> None:
    await send_to_rabbit_mq(
        message=json.dumps(
            {
                "status": 1,   # if 1 that new user
                "username": username,
                "email": email,
                "referralCode": referral_code,
                "referrer": referrer
            }
        )
    )
    await send_to_bot(
        message=(
            "New user\n"
            f"Username: {username}\n"
            f"Email: {email}\n"
            f"Referral code: {referral_code}\n"
            f"Referrer: {referrer if referrer is not None else 'Missing'}"
        )
    )
    await send_to_email(
        subject=f"Welcome '{username}' to our referral system!!!",
        message=f"Your referral code: {referral_code}\n{f'You have been acclaimed: {referrer}' if referrer is not None else ''}",
        email=email
    )

async def send_if_not_new(owner_email: str, owner_username: str, lvl: int, new_user: str) -> None:
    await send_to_email(
        subject=f"Hello, {owner_username}, you have a new referral!!!",
        message=f"Level: {lvl}\nUsername: {new_user}",
        email=owner_email
    )

async def if_not_new(referrer: str, new_user: str, lvl: int = 1) -> bool:
    result = await db.get_username_by_referral_code(referrer=referrer)
    ref_users = json.loads(result["ref_users"])
    if lvl >= 4:
        await send_if_not_new(
            owner_email=result["email"],
            owner_username=result["username"],
            lvl=4,
            new_user=new_user
        )
    else:
        await send_if_not_new(
            owner_email=result["email"],
            owner_username=result["username"],
            lvl=lvl,
            new_user=new_user
        )
    if result["referrer"] is not None:
        return await if_not_new(referrer=result["referrer"], new_user=new_user, lvl=lvl+1)
    return True