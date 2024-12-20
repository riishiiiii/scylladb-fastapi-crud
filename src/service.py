from .database import get_db_session
from .schema import User, UserResponse
import uuid


class UserNotFound(BaseException):
    def __init__(self):
        super().__init__("User not found")


class CrudService:

    def __init__(self) -> None:
        self.session = get_db_session()

    async def create_user(self, user: User) -> UserResponse:
        id = uuid.uuid4()
        insert_query = """
        INSERT INTO users (id, name, email, age) 
        VALUES (%s, %s, %s, %s)
        """

        self.session.execute(insert_query, (id, user.name, user.email, user.age))

        return UserResponse(id=id, name=user.name, email=user.email, age=user.age)

    async def read_user(self, user_id: uuid.UUID) -> User:
        select_query = "SELECT * FROM users WHERE id = %s"
        result = self.session.execute(select_query, [user_id])

        user = result.one()
        if not user:
            raise UserNotFound()

        return UserResponse(id=user.id, name=user.name, email=user.email, age=user.age)

    async def update_user(self, user_id: uuid.UUID, updated_user: User) -> UserResponse:
        update_query = """
        UPDATE users 
        SET name = %s, email = %s, age = %s 
        WHERE id = %s
        """

        self.session.execute(
            update_query,
            (updated_user.name, updated_user.email, updated_user.age, user_id),
        )
        return UserResponse(
            id=user_id,
            name=updated_user.name,
            email=updated_user.email,
            age=updated_user.age,
        )

    async def delete_user(self, user_id: uuid.UUID) -> None:
        delete_query = "DELETE FROM users WHERE id = %s"
        self.session.execute(delete_query, [user_id])

    async def list_users(self) -> list[UserResponse]:
        select_query = "SELECT * FROM users"
        result = self.session.execute(select_query)
        return [
            UserResponse(id=user.id, name=user.name, email=user.email, age=user.age)
            for user in result
        ]
