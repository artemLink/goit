from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import users as repositories_users
from src.schemas.user import UserSchema, TokenSchema, UserResponse, RequestEmail
from src.services.auth import auth_service

from src.services.email import send_email, send_email_password

router = APIRouter(prefix="/auth", tags=["auth"])
get_refresh_token = HTTPBearer()


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    body: UserSchema,
    bt: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user.

    :param body: User data to create a new user.
    :type body: UserSchema
    :param bt: BackgroundTasks to execute background tasks.
    :type bt: BackgroundTasks
    :param request: HTTP request object.
    :type request: Request
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: Newly created user.
    :rtype: UserResponse
    :raise HTTPException 409: If the account already exists.
    """

    exist_user = await repositories_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repositories_users.create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


@router.post("/login", response_model=TokenSchema)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user login.

    :param body: OAuth2 password request form containing user credentials.
    :type body: OAuth2PasswordRequestForm
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: Access and refresh tokens.
    :rtype: TokenSchema
    :raise HTTPException 401: If the email is invalid or the account is not confirmed.
    """

    user = await repositories_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Account not confirmed"
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repositories_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token", response_model=TokenSchema)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    db: AsyncSession = Depends(get_db),
):
    """
    Refresh authentication token.

    :param credentials: HTTP Authorization Credentials containing refresh token.
    :type credentials: HTTPAuthorizationCredentials
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: New access and refresh tokens.
    :rtype: TokenSchema
    :raise HTTPException 401: If the refresh token is invalid.
    """

    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repositories_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repositories_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repositories_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    Confirm user email.

    :param token: Email confirmation token.
    :type token: str
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: Confirmation message.
    :rtype: dict
    :raise HTTPException 400: If the email verification fails.
    """

    email = await auth_service.get_email_from_token(token)
    user = await repositories_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repositories_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Request email confirmation.

    :param body: Email request data.
    :type body: RequestEmail
    :param background_tasks: BackgroundTasks to execute background tasks.
    :type background_tasks: BackgroundTasks
    :param request: HTTP request object.
    :type request: Request
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: Confirmation message.
    :rtype: dict
    :raise HTTPException 400: If the email is already confirmed.
    """

    user = await repositories_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, str(request.base_url)
        )
    return {"message": "Check your email for confirmation."}


@router.post("/reset_password")
async def reset_password(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Reset user password.

    :param body: Email request data.
    :type body: RequestEmail
    :param background_tasks: BackgroundTasks to execute background tasks.
    :type background_tasks: BackgroundTasks
    :param request: HTTP request object.
    :type request: Request
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: Password reset message.
    :rtype: dict
    :raise HTTPException 400: If the user email is not found.
    """

    user = await repositories_users.get_user_by_email(body.email, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not found users email"
        )
    if user:
        background_tasks.add_task(
            send_email_password,
            user.email,
            user.username,
            str(request.base_url),
        )
    return {"message": "Check your email for change password."}


@router.get("/change_password/{token}")
async def change_password(
    token: str,
    password: str,
    confirm_password: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Change user password.

    :param token: Password change token.
    :type token: str
    :param password: New password.
    :type password: str
    :param confirm_password: Confirm new password.
    :type confirm_password: str
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: Password change confirmation message.
    :rtype: dict
    :raise HTTPException 400: If the password change fails.
    """

    email = await auth_service.get_email_from_token(token)
    user = await repositories_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password change error"
        )
    if password != confirm_password:
        return {"message": "Different passwords"}
    hashed_password = auth_service.get_password_hash(password)
    print(hashed_password)
    await repositories_users.change_password(user, hashed_password, db)
    return {"message": "Password change complete"}
