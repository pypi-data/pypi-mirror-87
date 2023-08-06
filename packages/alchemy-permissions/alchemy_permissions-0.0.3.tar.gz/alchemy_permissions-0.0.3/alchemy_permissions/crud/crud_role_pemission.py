from typing import List, Optional

from sqlalchemy import select

from app.crud.base import CRUDBase, UpdateSchemaType
from app.db.database import database

from alchemy_permissions.models import RolePermission
from alchemy_permissions.schemas import RolePermissionCreate, RolePermissionUpdate


class CRUDRolePermission(CRUDBase[RolePermission, RolePermissionCreate, RolePermissionUpdate]):

    async def update(self, data: UpdateSchemaType) -> None:
        raise NotImplementedError

    async def get_by_role(self, role_id: int) -> List[dict]:
        query = select([self.model]).where(self.model.role_id == role_id)
        role_permissions = await database.fetch_all(query)
        return [dict(x) for x in role_permissions] if len(role_permissions) > 0 else None

    async def get_by_role_and_permission(self, role_id: int, permission_id: int) -> Optional[dict]:
        query = (
            select([self.model])
            .where(
                (self.model.role_id == role_id) &
                (self.model.permission_id == permission_id)
            )
        )
        role_permission = await database.fetch_one(query)
        return dict(role_permission) if role_permission else None


role_permission = CRUDRolePermission(RolePermission)
