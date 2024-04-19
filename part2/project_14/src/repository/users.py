from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.database.db import get_db
from src.database.models import User
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a user by email from the database.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: AsyncSession object representing the database session. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: The retrieved user object, or None if not found.
    :rtype: User
    """

    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    Create a new user in the database.

    :param body: The schema representing the user data.
    :type body: UserSchema
    :param db: AsyncSession object representing the database session. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: The created user object.
    :rtype: User
    """

    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    Update the refresh token for a user in the database.

    :param user: The user object to update.
    :type user: User
    :param token: The new refresh token. Can be None.
    :type token: str | None
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    """

    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Set the email confirmation status for a user in the database to True.

    :param email: The email address of the user.
    :type email: str
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    """

    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    Update the avatar URL for a user in the database.

    :param email: The email address of the user.
    :type email: str
    :param url: The new avatar URL. Can be None.
    :type url: str | None
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :return: The updated user object.
    :rtype: User
    """

    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user


async def change_password(user: User, password: str, db: AsyncSession):
    """
    Change the password for a user in the database.

    :param user: The user object to update.
    :type user: User
    :param password: The new password.
    :type password: str
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :return: The updated user object.
    :rtype: User
    """

    user.password = password
    await db.commit()
    await db.refresh(user)
    return user
