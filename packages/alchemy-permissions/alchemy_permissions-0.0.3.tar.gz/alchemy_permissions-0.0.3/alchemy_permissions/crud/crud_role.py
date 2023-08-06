from typing import Optional, List

from sqlalchemy import select

from app.crud.base import CRUDBase, UpdateSchemaType
from app.db.database import database

from alchemy_permissions.enums import Roles
from alchemy_permissions.models import Role
from alchemy_permissions.schemas import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    async def update(self, data: UpdateSchemaType) -> None:
        raise NotImplementedError

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


role = CRUDRole(Role)
