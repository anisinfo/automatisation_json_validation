from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class Adresse(BaseModel):
    rue: str
    ville: str
    code_postal: str = Field(..., regex=r'^[0-9]{5}$')

class PydanticValidator:
    class UserModel(BaseModel):
        nom: str = Field(..., min_length=1)
        age: int = Field(..., gt=0)
        email: Optional[EmailStr] = None
        adresse: Optional[Adresse] = None

    @staticmethod
    def validate_user(data):
        try:
            user = PydanticValidator.UserModel(**data)
            return True, user
        except Exception as e:
            error_messages = []
            for error in e.errors():
                field = ".".join(str(loc) for loc in error['loc'])
                message = error['msg']
                error_messages.append(f"{field}: {message}")
            raise ValueError(" | ".join(error_messages))