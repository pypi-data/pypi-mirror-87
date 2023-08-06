from typing import Optional, List

from sqlalchemy import select

from app.crud.base import CRUDBase, UpdateSchemaType
from app.db.database import database

from alchemy_permissions.enums import Permissions
from alchemy_permissions.models import Permission
from alchemy_permissions.schemas import PermissionCreate, PermissionUpdate


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):

    async def update(self, data: UpdateSchemaType) -> None:
        raise NotImplementedError

    async def get_by_permission(self, permission_type: Permissions) -> Optional[dict]:
        query = select([self.model]).where(self.model.name == permission_type.name)
        permission = await database.fetch_one(query)
        return dict(permission) if permission else None

    async def get_all_permissions(self) -> List[dict]:
        """Получение списка всех пермишенов в системе."""
        permissions = await database.fetch_all(select([self.model]))
        if len(permissions) > 0:
            return [dict(x) for x in permissions]
        else:
            return []


permission = CRUDPermission(Permission)
