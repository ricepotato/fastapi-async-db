from sqlalchemy import orm
from app import database, schema, models


class AsyncUserRepository:
    def __init__(self, db: database.AsyncDatabase):
        self.db = db

    async def insert_user(self, user: models.UserCreate):
        async with self.db.session() as session:
            # addresses = user.addresses
            if user.addresses:
                _addresses = [
                    schema.Address(email_address=a.email_address)
                    for a in user.addresses
                ]
            new_user = schema.User(
                name=user.name, fullname=user.fullname, addresses=_addresses
            )
            session.add(new_user)
            await session.commit()
            return new_user.id

    async def get_user_by_id(self, user_id: int) -> models.User:
        async with self.db.session() as session:
            # select = (
            #     sqlalchemy.select(schema.User)
            #     .where(schema.User.id == user_id)
            #     .options(orm.selectinload(schema.User.addresses))
            # )
            # user = (await session.execute(select)).scalar_one_or_none()
            user_get = await session.get(
                schema.User,
                user_id,
                options=[
                    orm.selectinload(schema.User.addresses),
                ],
            )
            return models.User.from_orm(user_get)

    async def update_user(self, user: models.User):
        async with self.db.session() as session:
            user_update = await session.get(
                schema.User,
                user.id,
                options=[
                    orm.selectinload(schema.User.addresses),
                ],
            )
            user_update.name = user.name
            user_update.fullname = user.fullname

            if user.addresses:
                user_update.addresses = [
                    schema.Address(id=a.id, email_address=a.email_address)
                    for a in user.addresses
                ]
            await session.commit()
