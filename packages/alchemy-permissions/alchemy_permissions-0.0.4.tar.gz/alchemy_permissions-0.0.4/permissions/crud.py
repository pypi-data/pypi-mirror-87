from typing import Optional, List
from sqlalchemy import select

from backend.common.crud import CRUDBase
from backend.db.database import database

from permissions.enums import Permissions, Roles
from permissions.models import AccountRole, Permission, Role, RolePermission
from permissions.schemas import (
    AccountRoleCreate, AccountRoleUpdate,
    PermissionCreate, PermissionUpdate,
    RoleCreate, RoleUpdate, RolePermissionUpdate, RolePermissionCreate
)


class CRUDAccountRole(CRUDBase[AccountRole, AccountRoleCreate, AccountRoleUpdate]):

    async def get_by_account(self, account_id: int) -> Optional[dict]:
        query = select([self.model]).where(self.model.account_id == account_id)
        account_role = await database.fetch_one(query)
        return dict(account_role) if account_role else None


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):

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


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    async def get_by_role(self, role_type: Roles) -> Optional[dict]:
        query = select([self.model]).where(self.model.name == role_type.name)
        role = await database.fetch_one(query)
        return dict(role) if role else None

    async def get_all_roles(self) -> List[dict]:
        """
        Получение списка всех ролей в системе.
        В словарях хранится форма {'id': 1, 'name': 'CUSTOMER', 'description': 'Клиент'}
        """
        roles = await database.fetch_all(select([self.model]))
        if len(roles) > 0:
            return [dict(x) for x in roles]
        else:
            return []


class CRUDRolePermission(CRUDBase[RolePermission, RolePermissionCreate, RolePermissionUpdate]):

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


role = CRUDRole(Role)
permission = CRUDPermission(Permission)
account_role = CRUDAccountRole(AccountRole)
role_permission = CRUDRolePermission(RolePermission)
