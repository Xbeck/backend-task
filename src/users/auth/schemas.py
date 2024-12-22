from pydantic import BaseModel, ConfigDict, EmailStr



class AuthDTO(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "email": "test@test.com",
                "password": "test",
            }
        }
    )

