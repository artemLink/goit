from datetime import datetime, timedelta

from sqlalchemy import select, extract, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas.contact import ContactSchema


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """Створює новий контакт у базі даних."""

    contact = Contact(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """Повертає список контактів з бази даних з урахуванням ліміту та зміщення."""

    stmt = select(Contact).filter(Contact.user == user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """Повертає контакт за його ідентифікатором."""

    stmt = select(Contact).filter_by(id=contact_id, user=user)
    res = await db.execute(stmt)
    contact = res.scalar_one_or_none()
    if contact:
        return contact
    else:
        return None


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession, user: User):
    """Оновлює існуючий контакт у базі даних."""

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
    else:
        return None


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    """Видаляє контакт з бази даних за його ідентифікатором."""

    stmt = select(Contact).filter_by(id=contact_id, user=user)
    res = await db.execute(stmt)
    contact = res.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
        return contact
    else:
        return None


async def search(first_name: str, last_name: str, email: str, db: AsyncSession, user: User):
    """Пошук контактів за ім'ям, прізвищем та адресою електронної пошти."""

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
    """Повертає список контактів, у яких день народження протягом наступних 7 днів."""

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
