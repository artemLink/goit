from datetime import date

from pydantic import BaseModel, Field, field_validator


class ContactSchema(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str | None = Field(max_length=100, nullable=True)
    email: str | None = Field(max_length=100, nullable=True)
    phone_number: str = Field(max_length=20,
                              pattern=r"^\+\d{12}$")  # Приклад регулярного виразу для номера телефону
    birthday: date | None = Field(nullable=True)
    description: str | None = Field(max_length=250, nullable=True)

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if v is not None and not v.startswith("+"):
            raise ValueError("Номер телефону повинен починатися з '+'")
        return v

    @field_validator("birthday")
    def validate_birthday(cls, v):
        if v is not None and not isinstance(v, date):
            raise ValueError("Дата народження повинна бути типу date")
        if v is not None and v > date.today():
            raise ValueError("Дата народження не може бути в майбутньому")
        return v


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    description: str

    class Config:
        from_attributes = True
