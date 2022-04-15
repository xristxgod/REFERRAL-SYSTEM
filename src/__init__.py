import typing

import asyncpg

from config import Config


class DB:
    """
    <<<--------------------------------------------------->>>
    table = user_model
        id: Integer Primary Key
        username: String(256) NOT NULL UNIQUE = TRUE
        password: String(256) NOT NULL
        email: String(256) NOT NULL UNIQUE = TRUE
    <<<--------------------------------------------------->>>
    tabel = referral_model
        id: Integer Primary Key
        reg_time: Integer
        referral_code: String(60) NOT NULL UNIQUE = TRUE
        referrer: String(60) NULL
        ref_users: String(2048) NULL
        user_id: Integer ForeignKey(user_model.id)
    <<<--------------------------------------------------->>>
    """

    @staticmethod
    async def __select_method(sql):
        connection: asyncpg.Connection = None
        try:
            connection: asyncpg.Connection = await asyncpg.connect(Config)
            return await connection.fetch(sql)
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def __insert_method(sql):
        connection: asyncpg.Connection = None
        try:
            connection: asyncpg.Connection = await asyncpg.connect(Config.DATABASE_URL)
            await connection.execute(sql)
            return True
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def create_user(username: str, email: str, password: str) -> bool:
        """Create a new user"""
        return await DB.__insert_method((
            f"INSERT user_model (username, email, password) "
            f"VALUES ('{username}', '{email}', '{password}');"
        ))

    @staticmethod
    async def create_referral_by_user_id(
            user_id: int, referral_code: str, ref_users: str, reg_time: int, referrer: str = None
    ) -> bool:
        """Create a referral code for a new user"""
        return await DB.__insert_method((
            f"INSERT referral_model (referral_code, ref_users, reg_time, referrer, user_id) "
            f"VALUES ('{referral_code}', '{ref_users}', {reg_time}, '{referrer}', {user_id});"
        ))

    @staticmethod
    async def update_referral_lvl_by_user_id(user_id: int, ref_users: str) -> bool:
        """Update the user level."""
        return await DB.__insert_method((
            f"UPDATE referral_model SET ref_users='{ref_users}' "
            f"WHERE user_id={user_id};"
        ))

    @staticmethod
    async def get_user_id_by_username(username: str) -> int:
        """Return the user id by its username."""
        return (await DB.__select_method((
            f"SELECT id FROM user_model "
            f"WHERE username='{username}'"
        )))[0]

    @staticmethod
    async def get_referrer_by_referral_code(referral: str) -> typing.Dict:
        """Find out who owns this referral code."""
        return dict((await DB.__select_method((
            f"SELECT referral_code, referrer, ref_users, user_id FROM referral_model "
            f"WHERE referral_code='{referral}'"
        )))[0])

    @staticmethod
    async def get_referral_info_by_user_id(user_id: int) -> typing.Dict:
        """Get all the information about the user's referral system by his id."""
        return dict((await DB.__select_method((
            f"SELECT referral_code, referrer, ref_users, reg_time FROM referral_model "
            f"WHERE user_id={user_id}"
        )))[0])

    @staticmethod
    async def get_username_by_referral_code(referrer: str) -> typing.Dict:
        """Get information about the user by his referral code"""
        ref_info = await DB.get_referrer_by_referral_code(referral=referrer)
        user_info = dict((await DB.__select_method((
            f"SELECT username, email FROM user_model "
            f"WHERE id={ref_info['user_id']}"
        )))[0])
        return {
            **ref_info,
            **user_info
        }

db = DB