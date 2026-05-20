"""Pytest configuration and fixtures."""
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.models import Base


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db():
    """Create test database."""
    # Use in-memory SQLite for tests
    test_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )

    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session factory
    test_session_maker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with test_session_maker() as session:
        yield session

    # Cleanup
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()
