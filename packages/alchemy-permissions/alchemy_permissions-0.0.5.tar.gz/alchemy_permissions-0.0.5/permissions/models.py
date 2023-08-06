from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey

from backend.db.base_class import Base
from permissions.enums import Permissions, Roles


class Role(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), Enum(Roles), unique=True)
    description = Column(String(128))


class Permission(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), Enum(Permissions), unique=True)
    description = Column(String(128))


class RolePermission(Base):

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    permission_id = Column(Integer, ForeignKey("permission.id"))


class AccountRole(Base):
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    role_id = Column(Integer, ForeignKey("role.id"))