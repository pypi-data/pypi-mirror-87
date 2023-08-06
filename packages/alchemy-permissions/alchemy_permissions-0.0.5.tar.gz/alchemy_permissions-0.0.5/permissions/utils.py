from typing import Optional, List

from permissions import crud
from permissions.enums import Roles, Permissions
from permissions.schemas import AccountRoleCreate


async def _get_current_role(account_id: int) -> Optional[dict]:
    account_role = await crud.account_role.get_by_account(account_id)
    if not account_role:
        return None

    role = await crud.role.get(account_role['role_id'])
    if not role:
        return None

    return role


async def account_role(account_id: int) -> Optional[Roles]:
    role = await _get_current_role(account_id)
    if not role:
        return None

    return Roles(role['description'])


async def is_have_permission(account_id: int, required_permissions: List[Permissions]) -> bool:
    role = await _get_current_role(account_id)

    role_permissions = await crud.role_permission.get_by_role(role['id'])
    if len(role_permissions) == 0:
        return False

    permissions = list()

    for role_permission in role_permissions:
        permission = await crud.permission.get(role_permission['permission_id'])
        if not permission:
            continue
        permissions.append(permission['name'])

    return set([x.name for x in required_permissions]).issubset(set(permissions))


async def create_account_role(account_id: int, role: Roles) -> Roles:
    account_role = await crud.account_role.get_by_account(account_id)
    if account_role:
        return account_role

    role_object = await crud.role.get_by_role(role)
    if not role_object:
        raise ValueError("Role is not found")

    schema = AccountRoleCreate(account_id=account_id, role_id=role_object['id'])
    await crud.account_role.create(schema)

    return Roles(role_object['description'])
