from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class AccountRole(Base):
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    role_id = Column(Integer, ForeignKey("role.id"))