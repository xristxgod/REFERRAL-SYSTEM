from src.db import db
from src.services import search_by_ref_code, get_user_information
from src.utils import generate_referral_code, get_datetime_now

async def reg_new_user(username: str, email: str, password: str, referrer: str = None) -> bool:
    """
    Function for registering a new user.
    :param referrer: The referral code of the invitee
    """
    await db.create_user(username=username, password=password, email=email)
    user_id = await db.get_user_id_by_username(username=username)
    if not referrer:
        return await db.create_referral_by_user_id(
            user_id=user_id,
            reg_time=get_datetime_now(),
            referral_code=generate_referral_code(),
            ref_users='{"lvl_1": [], "lvl_2": [], "lvl_3": [], "lvl_4": []}'
        )
    await db.create_referral_by_user_id(
        user_id=user_id,
        reg_time=get_datetime_now(),
        referral_code=generate_referral_code(),
        ref_users='{"lvl_1": [], "lvl_2": [], "lvl_3": [], "lvl_4": []}',
        referrer=referrer
    )
    return await search_by_ref_code(referrer=referrer, user_id=user_id)

async def get_user(username: str):
    return await get_user_information(user_id=(await db.get_user_id_by_username(username=username)), username=username)