from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict

from src.schemas.user import UserResponse


class ContactSchema(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str | None = Field(max_length=100, json_schema_extra={"nullable": True})
    email: str | None = Field(max_length=100, json_schema_extra={"nullable": True})
    phone_number: str = Field(max_length=20)
    birthday: date | None = Field(json_schema_extra={"nullable": True})
    description: str | None = Field(max_length=250, json_schema_extra={"nullable": True})

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
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    model_config = ConfigDict(from_attributes=True)
