from pydantic import BaseModel
from .base import UpdateBase


class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int


class RolePermissionUpdate(UpdateBase):
    pass
