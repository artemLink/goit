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
    try:
        return await repositories_contacts.create_contact(body, db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'{e}')


@router.get('/', response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contacts(limit: int = Query(10, ge=10, le=500),
                       offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    return await repositories_contacts.get_contacts(limit, offset, db, user)


@router.get('/all', response_model=list[ContactResponse], dependencies=[Depends(access_to_route_all)])
async def get_all_contacts(limit: int = Query(10, ge=10, le=500),
                           offset: int = Query(0, ge=0),
                           db: AsyncSession = Depends(get_db)):
    return await repositories_contacts.get_all_contacts(limit, offset, db)


@router.get("/search", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def search_contacts(first_name: str = Query(None), last_name: str = Query(None), email: str = Query(None),
                          db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    return await repositories_contacts.search(first_name, last_name, email, db, user)


@router.get("/birthdays/", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_birthdays(db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    birth_search = await repositories_contacts.upcoming_birthday(db, user)
    if not birth_search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No upcoming birthdays')
    return birth_search


@router.get('/{contact_id}', response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Contact with id {contact_id} not found')
    return contact


@router.put('/{contact_id}', dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Contact with id {contact_id} not found')
    return contact


@router.delete("/{contact_id}", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.delete_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Contact with id {contact_id} not found')
    return contact
