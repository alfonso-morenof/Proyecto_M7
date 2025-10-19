# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from api.main import app

# Fixture asíncrona que expone un cliente HTTPX contra la app ASGI
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)  # <-- aquí conectamos la app FastAPI
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
