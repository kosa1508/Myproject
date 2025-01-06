from sqlalchemy import select
from pydantic import EmailStr

from src.Schemas.users import User, UserWithHashedPassword
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository

class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)

























