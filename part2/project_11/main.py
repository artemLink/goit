from fastapi import FastAPI, HTTPException, Query
from models import Contact, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

engine = create_engine('postgresql://postgres:123@localhost:5432/contact')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@app.post("/api/add_contact")
async def root(first_name, last_name, email, phone_number, birthday, additional_info=None):
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                          birthday=birthday, additional_info=additional_info)

    session.add(new_contact)

    try:
        session.commit()
        return {"success": "True"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.get("/api/show_contacts")
async def show_contacts():
    contacts = session.query(Contact).all()
    return [contact.__dict__ for contact in contacts]


@app.get("/api/show_contact")
async def show_contact(contact_id):
    contact = session.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.delete("/api/delete_contact")
async def delete_contact(contact_id: int):
    # Пытаемся найти контакт по его ID
    contact = session.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    else:
        session.delete(contact)
        session.commit()
        return {"success": "True"}


class UpdatedContact(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: str
    additional_info: str = None


@app.put("/api/update_contact")
async def update_contact(contact_id: int, updated_contact: UpdatedContact):
    contact = session.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:

        raise HTTPException(status_code=404, detail="Contact not found")
    else:
        contact.first_name = updated_contact.first_name
        contact.last_name = updated_contact.last_name
        contact.email = updated_contact.email
        contact.phone_number = updated_contact.phone_number
        contact.birthday = updated_contact.birthday
        contact.additional_info = updated_contact.additional_info

        session.commit()
        return {"success": "True"}


@app.get("/api/contact_card/")
async def get_contact_card(
    query: str = Query(None, min_length=3, description="Search query (minimum 3 characters)")):
    if not query:
        raise HTTPException(status_code=400, detail="At least one search criteria must be provided")

    contact = session.query(Contact).filter(
        (Contact.first_name.ilike(f'%{query}%')) |
        (Contact.last_name.ilike(f'%{query}%')) |
        (Contact.email.ilike(f'%{query}%'))
    ).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {
        "id": contact.id,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "email": contact.email,
        "phone_number": contact.phone_number,
        "birthday": contact.birthday,
        "additional_info": contact.additional_info
    }


@app.get("/api/upcoming_birthdays/")
async def get_upcoming_birthdays():
    current_date = datetime.now().date()

    future_date = current_date + timedelta(days=7)

    upcoming_birthdays = session.query(Contact).filter(
        Contact.birthday.between(current_date, future_date)
    ).all()

    if upcoming_birthdays:
        return [
            {
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "email": contact.email,
                "phone_number": contact.phone_number,
                "birthday": contact.birthday,
                "additional_info": contact.additional_info
            }
            for contact in upcoming_birthdays
        ]
    else:
        raise HTTPException(status_code=404, detail="No upcoming birthdays found")