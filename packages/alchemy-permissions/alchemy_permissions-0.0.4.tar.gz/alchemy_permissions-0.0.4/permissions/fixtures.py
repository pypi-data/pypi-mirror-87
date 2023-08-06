from structlog import get_logger

from permissions import crud
from permissions.enums import Roles, Permissions
from permissions.schemas import RoleCreate, PermissionCreate, RolePermissionCreate


async def setup_permissions_and_roles():
    """
    Обновляет права доступа у ролей системы.
    """
    logger = get_logger()

    logger.info(f"Settings up permissions and roles")
    for role_enum in Roles:
        role_data = await crud.role.get_by_role(role_enum)
        if not role_data:
            await crud.role.create(RoleCreate(name=role_enum.name, description=role_enum.description))
            logger.info(f'Role is created', name=role_enum.name, description=role_enum.description)

    for permission_enum in Permissions:  # Устанавливаем роли в системе
        permission_id = await crud.permission.get_by_permission(permission_enum)
        if not permission_id:
            await crud.permission.create(PermissionCreate(name=permission_enum.name, description=permission_enum.description))
            logger.info(f'Permissions is created', name=permission_enum.name, description=permission_enum.description)

    roles = await crud.role.get_all_roles()

    for role in roles:  # Простоявляем ограничения установленные в permission_list
        try:
            role_enum = Roles(role['description'])
        except ValueError:
            continue

        permissions_list = role_enum.get_permissions()
        for permission_enum in permissions_list:
            permission = await crud.permission.get_by_permission(permission_enum)
            if permission:
                role_permission = await crud.role_permission.get_by_role_and_permission(
                    role_id=role['id'], permission_id=permission['id']
                )
                if not role_permission:
                    await crud.role_permission.create(
                        data=RolePermissionCreate(role_id=role['id'], permission_id=permission['id'])
                    )
                    logger.info("Permission added to role", role=role['name'], permission=permission['name'])