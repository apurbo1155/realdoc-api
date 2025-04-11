from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
import logging

logger = logging.getLogger(__name__)

async def get_mongo_client():
    """Create and return a new MongoDB client instance"""
    try:
        from realdoc_api.config import MONGO_URI, MONGO_DB_NAME
    except ImportError:
        from config import MONGO_URI, MONGO_DB_NAME

    client = AsyncIOMotorClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=30000,
        retryWrites=True,
        retryReads=True
    )
    try:
        await client.admin.command('ping')
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise RuntimeError("MongoDB connection failed") from e

async def get_db(client: AsyncIOMotorClient = Depends(get_mongo_client)):
    """Get the database instance from a client"""
    try:
        from realdoc_api.config import MONGO_DB_NAME
    except ImportError:
        from config import MONGO_DB_NAME
        
    return client[MONGO_DB_NAME]
