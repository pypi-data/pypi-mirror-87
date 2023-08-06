from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class RolePermission(Base):

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    permission_id = Column(Integer, ForeignKey("permission.id"))
