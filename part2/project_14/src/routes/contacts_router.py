from fastapi import APIRouter, Depends, Query, HTTPException, status, Path
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Role
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactResponse, ContactSchema
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix='/contacts', tags=['contacts'])

access_to_route_all = RoleAccess([Role.admin, Role.moderator])


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=1, seconds=5))])
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    Create a new contact.

    :param body: Contact data to create a new contact.
    :type body: ContactSchema
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :param user: The current user making the request.
    :type user: User
    :return: Newly created contact.
    :rtype: ContactResponse
    :raise HTTPException 409: If the contact creation fails due to conflict.
    """

    try:
        return await repositories_contacts.create_contact(body, db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'{e}')


@router.get('/', response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contacts(limit: int = Query(10, ge=10, le=500),
                       offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a list of contacts.

    :param limit: Maximum number of contacts to retrieve. Defaults to 10, maximum 500.
    :type limit: int
    :param offset: Number of contacts to skip.
    :type offset: int
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :param user: The current user making the request.
    :type user: User
    :return: List of contacts.
    :rtype: list[ContactResponse]
    """

    return await repositories_contacts.get_contacts(limit, offset, db, user)


@router.get('/all', response_model=list[ContactResponse], dependencies=[Depends(access_to_route_all)])
async def get_all_contacts(limit: int = Query(10, ge=10, le=500),
                           offset: int = Query(0, ge=0),
                           db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all contacts (for admins and moderators only).

    :param limit: Maximum number of contacts to retrieve. Defaults to 10, maximum 500.
    :type limit: int
    :param offset: Number of contacts to skip.
    :type offset: int
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :return: List of contacts.
    :rtype: list[ContactResponse]
    """

    return await repositories_contacts.get_all_contacts(limit, offset, db)


@router.get("/search", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def search_contacts(first_name: str = Query(None), last_name: str = Query(None), email: str = Query(None),
                          db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    Search contacts by first name, last name, or email.

    :param first_name: First name to search for.
    :type first_name: str
    :param last_name: Last name to search for.
    :type last_name: str
    :param email: Email to search for.
    :type email: str
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :param user: The current user making the request.
    :type user: User
    :return: List of matching contacts.
    :rtype: list[ContactResponse]
    """

    return await repositories_contacts.search(first_name, last_name, email, db, user)


@router.get("/birthdays/", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_birthdays(db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve upcoming birthdays.

    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :param user: The current user making the request.
    :type user: User
    :return: List of contacts with upcoming birthdays.
    :rtype: list[ContactResponse]
    :raise HTTPException 404: If no upcoming birthdays are found.
    """

    birth_search = await repositories_contacts.upcoming_birthday(db, user)
    if not birth_search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No upcoming birthdays')
    return birth_search


@router.get('/{contact_id}', response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a specific contact by ID.

    :param contact_id: ID of the contact to retrieve.
    :type contact_id: int
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :param user: The current user making the request.
    :type user: User
    :return: The retrieved contact.
    :rtype: ContactResponse
    :raise HTTPException 404: If the specified contact is not found.
    """

    contact = await repositories_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Contact with id {contact_id} not found')
    return contact


@router.put('/{contact_id}', dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    Update a specific contact by ID.

    :param body: Contact data for updating the contact.
    :type body: ContactSchema
    :param contact_id: ID of the contact to update.
    :type contact_id: int
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :param user: The current user making the request.
    :type user: User
    :return: The updated contact.
    :rtype: ContactResponse
    :raise HTTPException 404: If the specified contact is not found.
    """

    contact = await repositories_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Contact with id {contact_id} not found')
    return contact


@router.delete("/{contact_id}", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    Delete a specific contact by ID.

    :param contact_id: ID of the contact to delete.
    :type contact_id: int
    :param db: Database session object. Defaults to Depends(get_db).
    :type db: AsyncSession
    :param user: The current user making the request.
    :type user: User
    :return: The deleted contact.
    :rtype: ContactResponse
    :raise HTTPException 404: If the specified contact is not found.
    """

    contact = await repositories_contacts.delete_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Contact with id {contact_id} not found')
    return contact
