import json

from src.db import db
from src.utils import get_datetime_now, is_there_user
from datetime import datetime

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

async def get_user_information(user_id: int, username: str):
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
