import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from src.restapi_create import app
from src.models import Product
from jose import jwt
from src.config import Config

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c

@pytest.fixture(scope="module")
async def 

@pytest.mark.anyio
async def test_create_user(client: AsyncClient):  # nosec
    Authorization = jwt.encode({"username": "admin", "email": "example@gmail.com"},
                                Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    response = await client.post("/create-product", json=)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "admin"
    assert "id" in data
    user_id = data["id"]
    user_obj = await Product.get(id=user_id)
    assert user_obj.id == user_id
