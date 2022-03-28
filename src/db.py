import typing

import asyncpg

from config import DATABASE_URL

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
    async def create_user(username: str, email: str, password: str) -> bool:
        """Create a new user"""
        connection: asyncpg.Connection = None
        try:
            connection: asyncpg.Connection = await asyncpg.connect(DATABASE_URL)
            await connection.execute(
                f"INSERT user_model (username, email, password) VALUES ('{username}', '{email}', '{password}');"
            )
            return True
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def create_referral_by_user_id(
            user_id: int, referral_code: str, ref_users: str, reg_time: int, referrer: str = None
    ) -> bool:
        """Create a referral code for a new user"""
        connection: asyncpg.Connection = None
        try:
            connection: asyncpg.Connection = await asyncpg.connect(DATABASE_URL)
            await connection.execute((
                f"INSERT referral_model (referral_code, ref_users, reg_time, referrer, user_id) "
                f"VALUES ('{referral_code}', '{ref_users}', {reg_time}, '{referrer}', {user_id});"
            ))
            return True
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def update_referral_lvl_by_user_id(user_id: int, ref_users: str) -> bool:
        """Update the user level."""
        connection: asyncpg.Connection = None
        try:
            connection: asyncpg.Connection = await asyncpg.connect(DATABASE_URL)
            await connection.execute(
                f"UPDATE referral_model SET ref_users='{ref_users}' WHERE user_id={user_id};"
            )
            return True
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def get_user_id_by_username(username: str) -> int:
        """Return the user id by its username."""
        connection: asyncpg.Connection = None
        try:
            connection: asyncpg.Connection = await asyncpg.connect(DATABASE_URL)
            return (await connection.fetch(
                f"SELECT id FROM user_model WHERE username='{username}'"
            ))[0]
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def get_referrer_by_referral_code(referral: str) -> typing.Dict:
        """Find out who owns this referral code."""
        connection: asyncpg.Connection = None
        try:
            connection: asyncpg.Connection = await asyncpg.connect(DATABASE_URL)
            return dict((await connection.fetch(
                f"SELECT referral_code, referrer, ref_users, user_id FROM referral_model WHERE referral_code='{referral}'"
            ))[0])
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def get_referral_info_by_user_id(user_id: int) -> typing.Dict:
        """Get all the information about the user's referral system by his id."""
        connection: asyncpg.Connection = None
        try:
            connection: asyncpg.Connection = await asyncpg.connect(DATABASE_URL)
            return dict((await connection.fetch(
                f"SELECT referral_code, referrer, ref_users, reg_time FROM referral_model WHERE user_id={user_id}"
            ))[0])
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

    @staticmethod
    async def get_username_by_referral_code(referrer: str) -> typing.Dict:
        """Get information about the user by his referral code"""
        connection: asyncpg.Connection = None
        ref_info = await DB.get_referrer_by_referral_code(referral=referrer)
        try:
            connection: asyncpg.Connection = await asyncpg.connect(DATABASE_URL)
            user_info = dict((await connection.fetch(
                f"SELECT username, email FROM user_model WHERE id={ref_info['user_id']}"
            ))[0])
            return {**ref_info, **user_info}
        except Exception as error:
            raise error
        finally:
            if connection is not None:
                await connection.close()

db = DB