from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
import logging

# Try multiple import approaches
try:
    from realdoc_api.config import MONGO_URI, MONGO_DB_NAME
except ImportError:
    try:
        from ..config import MONGO_URI, MONGO_DB_NAME  # Relative import
    except ImportError:
        from config import MONGO_URI, MONGO_DB_NAME  # Direct import

logger = logging.getLogger(__name__)

async def get_mongo_client():
    client = AsyncIOMotorClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=30000
    )
    try:
        await client.admin.command('ping')
        return client
    except Exception as e:
        logger.error(f"MongoDB connection failed: {str(e)}")
        raise RuntimeError("MongoDB connection failed") from e

async def get_db(client: AsyncIOMotorClient = Depends(get_mongo_client)):
    return client[MONGO_DB_NAME]