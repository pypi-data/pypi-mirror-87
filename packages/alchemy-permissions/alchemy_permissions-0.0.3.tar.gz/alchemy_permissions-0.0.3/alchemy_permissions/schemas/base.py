from pydantic import BaseModel


class CreateBaseEnum(BaseModel):
    name: str
    description: str


class UpdateBase(BaseModel):
    pass
