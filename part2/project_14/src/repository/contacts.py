from datetime import datetime, timedelta

from sqlalchemy import select, extract, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas.contact import ContactSchema


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
    Create a new contact in the database.

    :param body: The schema representing the contact data.
    :type body: ContactSchema
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :param user: The user to whom the contact belongs.
    :type user: User
    :return: The created contact object.
    :rtype: Contact
    """

    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """
    Retrieve a list of contacts from the database with limit and offset applied.

    :param limit: The maximum number of contacts to retrieve.
    :type limit: int
    :param offset: The offset from which to start retrieving contacts.
    :type offset: int
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :param user: The user whose contacts are to be retrieved.
    :type user: User
    :return: List of contacts retrieved from the database.
    :rtype: list[Contact]
    """

    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    """
    Retrieve a list of all contacts from the database with limit and offset applied.

    :param limit: The maximum number of contacts to retrieve.
    :type limit: int
    :param offset: The offset from which to start retrieving contacts.
    :type offset: int
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :return: List of all contacts retrieved from the database.
    :rtype: list[Contact]
    """

    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
    Retrieve a contact by its identifier.

    :param contact_id: The identifier of the contact to retrieve.
    :type contact_id: int
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :param user: The user to whom the contact belongs.
    :type user: User
    :return: The retrieved contact object, or None if not found.
    :rtype: Contact
    """

    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    """
    Update an existing contact in the database.

    :param contact_id: The identifier of the contact to update.
    :type contact_id: int
    :param body: The schema representing the updated contact data.
    :type body: ContactSchema
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :param user: The user to whom the contact belongs.
    :type user: User
    :return: The updated contact object, or None if not found.
    :rtype: Contact
    """

    stmt = select(Contact).filter_by(id=contact_id, user=user)
    res = await db.execute(stmt)
    contact = res.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.description = body.description
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    """
    Delete a contact from the database by its identifier.

    :param contact_id: The identifier of the contact to delete.
    :type contact_id: int
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :param user: The user to whom the contact belongs.
    :type user: User
    :return: The deleted contact object, or None if not found.
    :rtype: Contact
    """

    stmt = select(Contact).filter_by(id=contact_id, user=user)
    res = await db.execute(stmt)
    contact = res.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search(first_name: str, last_name: str, email: str, db: AsyncSession, user: User):
    """
    Search for contacts by first name, last name, or email address.

    :param first_name: The first name to search for.
    :type first_name: str
    :param last_name: The last name to search for.
    :type last_name: str
    :param email: The email address to search for.
    :type email: str
    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :param user: The user whose contacts are being searched.
    :type user: User
    :return: List of contacts matching the search criteria.
    :rtype: list[Contact]
    """

    stmt = None

    if first_name:
        stmt = select(Contact).filter(Contact.first_name.ilike(f"%{first_name}%"), Contact.user == user)
    if last_name:
        stmt = select(Contact).filter(Contact.last_name.ilike(f"%{last_name}%"), Contact.user == user)
    if email:
        stmt = select(Contact).filter(Contact.email.ilike(f"%{email}%"), Contact.user == user)

    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def upcoming_birthday(db: AsyncSession, user: User):
    """
    Retrieve contacts whose birthdays fall within the next 7 days.

    :param db: AsyncSession object representing the database session.
    :type db: AsyncSession
    :param user: The user whose contacts are being checked.
    :type user: User
    :return: List of contacts with birthdays in the next 7 days.
    :rtype: list[Contact]
    """

    today = datetime.today().date()
    week_from_now = today + timedelta(days=7)

    # Запит до бази даних для отримання контактів з днями народження у межах наступних 7 днів
    stmt = select(Contact).filter(
        or_(
            and_(
                extract('month', Contact.birthday) == today.month,
                extract('day', Contact.birthday) >= today.day,
            ),
            and_(
                extract('month', Contact.birthday) == week_from_now.month,
                extract('day', Contact.birthday) <= week_from_now.day
            )
        ),
        Contact.user == user
    )

    contacts = await db.execute(stmt)
    return contacts.scalars().all()
