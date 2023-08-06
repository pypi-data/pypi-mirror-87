# Alchemy permissions
Custom system of roles and permissions

This library is fine if you are using:
- SQLAlchemy ORM
- Database connector
- Alembic migrator
- Write code in style https://github.com/tiangolo/full-stack-fastapi-postgresql

### Requirements
You must have a class with a config in the system, which will be located in the app.core.config path.

This architecture is based on the analogy with the project
https://github.com/tiangolo/full-stack-fastapi-postgresql

#### Step #1 Add app.core.config
```sh
import secrets
from pydantic import BaseSettings

class Settings(BaseSettings)
    ....
    roles = Roles  # class Enum
    permissions = Permissions  # class Enum
```

#### Step #2 Add class Enum with roles and permissions
```sh
class Roles(Enum):

    customer = "Customer"
    admin = "Admin"

    @property
    def description(self):
        if self is self.customer:
            return "Customer"
        elif self is self.admin:
            return "Admin"

    def get_permissions(self):
        if self is self.customer:
            return [x for x in Permissions if x != Permissions.admin_api_access]
        elif self is self.admin:
            return [x for x in Permissions if x != Permissions.public_api_access]


class Permissions(Enum):

    public_api_access = "public_api_access"
    admin_api_access = "admin_api_access"

    @property
    def description(self):
        if self is self.public_api_access:
            return "Access to all api methods on the client side."
        elif self is self.admin_api_access:
            return "Access to all api methods for the administrator."
```
Need have base CRUD class in app.crud.base
https://github.com/tiangolo/full-stack-fastapi-postgresql
```
from app.crud.base import CRUDBase, UpdateSchemaType

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get():
        ....

```
You must use the databases library as a connector to the database.
https://fastapi.tiangolo.com/advanced/async-sql-databases/
```sh
pip install databases
```
Need have connector in app.db.database
```sh
database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
```
#### Step #3 Add model Account with custom fields
```sh
class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
```
#### Step #4 Add models in project.

Need add import in app.db.base.py
```shell script
from permissions import Role, RolePermission, AccountRole
```
#### Step #5 Make migrations
```sh
alembic revision --autogenerate -m "add permissions"
alembic upgrade head
```

### Using
#### Fixtures
To install roles and rights to the system, you need to run the fixture when the application starts

Need add in main.py
```sh
from alchemy_permissions.fixtures import setup_permissions_and_roles

@app.on_event("startup")
async def startup():
    await database.connect()
    await setup_permissions_and_roles()
```
Result
```shell script
2020-12-03 14:35.52 Settings up permissions and roles
2020-12-03 14:35.52 Role is created                description=Customer name=customer
2020-12-03 14:35.52 Role is created                description=Admin name=admin
2020-12-03 14:35.52 Permissions is created         description=Access to all api methods on the client side. name=public_api_access
2020-12-03 14:35.52 Permissions is created         description=Access to all api methods for the administrator. name=admin_api_access
2020-12-03 14:35.52 Permission added to role       permission=public_api_access role=customer
2020-12-03 14:35.52 Permission added to role       permission=admin_api_access role=admin
```

#### Binding a role to a user
The method binds the user to a role in the system and returns class Enum(Role)
```sh
await create_account_role(account_id, Roles.customer)  # return class Enum(Role)
```
#### Get current role a user
```sh
await account_role(account_id)  # return class Enum(Role)
```
#### Check user permission
Checking for access rights
```sh
await is_have_permission(current_account_id, [Permissions.public_api_access])  # return bool
```
