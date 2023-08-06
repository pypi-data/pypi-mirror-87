from typing import Optional

from sqlalchemy import select

from app.crud.base import CRUDBase, UpdateSchemaType
from app.db.database import database

from alchemy_permissions.models import AccountRole
from alchemy_permissions.schemas import AccountRoleCreate, AccountRoleUpdate


class CRUDAccountRole(CRUDBase[AccountRole, AccountRoleCreate, AccountRoleUpdate]):

    async def update(self, data: UpdateSchemaType) -> None:
        raise NotImplementedError

    async def get_by_account(self, account_id: int) -> Optional[dict]:
        query = select([self.model]).where(self.model.account_id == account_id)
        account_role = await database.fetch_one(query)
        return dict(account_role) if account_role else None


account_role = CRUDAccountRole(AccountRole)
