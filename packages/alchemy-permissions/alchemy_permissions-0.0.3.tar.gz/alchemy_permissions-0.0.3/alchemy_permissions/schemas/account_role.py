from pydantic import BaseModel
from .base import UpdateBase


class AccountRoleCreate(BaseModel):
    role_id: int
    account_id: int


class AccountRoleUpdate(UpdateBase):
    pass
