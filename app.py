from src import db
from src.services import search_by_ref_code, get_user_information, send_to
from src.utils import utils

async def reg_new_user(username: str, email: str, password: str, referrer: str = None) -> bool:
    """
    Function for registering a new user.
    :param referrer: The referral code of the invitee
    """
    create = False
    try:
        await db.create_user(username=username, password=password, email=email)
        user_id = await db.get_user_id_by_username(username=username)
        if not referrer:
            return await db.create_referral_by_user_id(
                user_id=user_id,
                reg_time=utils.get_datetime_now(),
                referral_code=utils.generate_referral_code(),
                ref_users='{"lvl_1": [], "lvl_2": [], "lvl_3": [], "lvl_4": []}'
            )
        await db.create_referral_by_user_id(
            user_id=user_id,
            reg_time=utils.get_datetime_now(),
            referral_code=utils.generate_referral_code(),
            ref_users='{"lvl_1": [], "lvl_2": [], "lvl_3": [], "lvl_4": []}',
            referrer=referrer
        )
        create = True
        return await search_by_ref_code(referrer=referrer, user_id=user_id)
    except Exception as error:
        raise error
    finally:
        if create:
            await send_to(username=username, referrer=referrer, email=email)

async def get_user(username: str):
    return await get_user_information(user_id=(await db.get_user_id_by_username(username=username)), username=username)