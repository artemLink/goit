import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.repository.contacts import (
    get_contact,
    get_contacts,
    get_all_contacts,
    create_contact,
    update_contact,
    delete_contact,
    search,
    upcoming_birthday
)
from src.schemas.contact import ContactSchema


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.user = User(id=1, username="test_user", password="password", email="test_user@email.com", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contact(self):
        contact = Contact(id=1, first_name="test", last_name="test", email="test@email.com", phone_number="+1234567890",
                          birthday=datetime.now().date(), description="test")
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(1, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(id=1, first_name="test", last_name="test", email="test@email.com", phone_number="+1234567890",
                    birthday=datetime.now().date(), description="test"),
            Contact(id=2, first_name="test", last_name="test", email="test@email.com", phone_number="+1234567890",
                    birthday=datetime.now().date(), description="test")]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_all_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(id=1, first_name="test", last_name="test", email="test@email.com", phone_number="+1234567890",
                    birthday=datetime.now().date(), description="test"),
            Contact(id=2, first_name="test", last_name="test", email="test@email.com", phone_number="+1234567890",
                    birthday=datetime.now().date(), description="test")]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactSchema(first_name="test", last_name="test", email="test@email.com", phone_number="+1234567890",
                             birthday=datetime.now().date(), description="test")
        result = await create_contact(body, self.session, self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)

    async def test_update_contact(self):
        body = ContactSchema(first_name="test", last_name="test", email="test@email.com", phone_number="+1234567890",
                             birthday=datetime.now().date(), description="test")
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, first_name="test", last_name="test",
                                                                 email="test@email.com", phone_number="1234567890",
                                                                 birthday=datetime.now().date(), description="test")
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)

    async def test_delete_contact(self):
        contact = Contact(id=1, first_name="test", last_name="test", email="test@email.com", phone_number="+1234567890",
                          birthday=datetime.now().date(), description="test")
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)

    async def test_search(self):
        contact = Contact(id=1, first_name="test", last_name="test", email="test@email.com", phone_number="+1234567890",
                          birthday=datetime.now().date(), description="test")
        mocked_contact = MagicMock()
        mocked_contact.scalars.return_value.all.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await search("test", "test", "test@email.com", self.session, self.user)
        self.assertEqual(result.first_name, contact.first_name)
        self.assertEqual(result.last_name, contact.last_name)
        self.assertEqual(result.email, contact.email)

    async def test_upcoming_birthday(self):
        today = datetime.now()
        date_1 = today + timedelta(days=1)
        date_2 = today + timedelta(days=6)
        date_3 = today - timedelta(days=3)
        contacts = [
            Contact(id=1, first_name="John", last_name="Doe", email="john@example.com",
                    phone_number="+1234567890", birthday=date_1.date(),
                    description="Friend"),
            Contact(id=2, first_name="Jane", last_name="Doe", email="jane@example.com",
                    phone_number="+1234567890", birthday=date_2.date(),
                    description="Family"),
            Contact(id=3, first_name="Alice", last_name="Smith", email="alice@example.com",
                    phone_number="+1234567890", birthday=date_3.date(),
                    description="Colleague"),
        ]

        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await upcoming_birthday(self.session, self.user)
        self.assertIsInstance(result, list)
        self.assertTrue(all(contact in result for contact in contacts[:2]))  # The first two contacts are in the result

