import pytest

from app import database, repository, models


@pytest.mark.asyncio
async def test_create_db(sqlite_db: database.AsyncDatabase):
    pass


@pytest.mark.asyncio
async def test_insert_and_get_user(repo: repository.AsyncUserRepository):
    new_user = get_new_user()
    user_id = await repo.insert_user(new_user)
    assert user_id

    get_user = await repo.get_user_by_id(user_id)
    assert get_user.name == new_user.name


@pytest.mark.asyncio
async def test_update_user(repo: repository.AsyncUserRepository):
    new_user = get_new_user()
    user_id = await repo.insert_user(new_user)
    assert user_id

    get_user = await repo.get_user_by_id(user_id)
    assert get_user.name == new_user.name

    get_user.name = "John Doe 2"
    get_user.addresses[0].email_address = "hello3@abc.dec"
    get_user.addresses.append(models.Address(email_address="hello4@abc.dec"))
    await repo.update_user(get_user)

    get_user = await repo.get_user_by_id(user_id)
    assert get_user.name == "John Doe 2"
    assert get_user.addresses[0].email_address == "hello3@abc.dec"
    assert get_user.addresses[2].email_address == "hello4@abc.dec"


def get_new_user():
    addresses = [
        models.Address(email_address="hello1@abc.dec"),
        models.Address(email_address="hello2@abc.dec"),
    ]
    return models.UserCreate(name="John", fullname="John Doe", addresses=addresses)
