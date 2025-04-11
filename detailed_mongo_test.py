import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, MONGO_DB_NAME
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_connection():
    try:
        logger.info(f"Attempting to connect with URI: {MONGO_URI}")
        logger.info(f"Database name: {MONGO_DB_NAME}")
        
        client = AsyncIOMotorClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=30000
        )
        
        logger.info("Testing connection...")
        await client.admin.command('ping')
        logger.info("✓ Successfully pinged MongoDB server")
        
        db = client[MONGO_DB_NAME]
        logger.info("Testing basic operations...")
        
        # Test insert
        result = await db.test_collection.insert_one({"test": "value"})
        logger.info(f"✓ Insert test document with id: {result.inserted_id}")
        
        # Test find
        doc = await db.test_collection.find_one({"_id": result.inserted_id})
        logger.info(f"✓ Found test document: {doc}")
        
        # Clean up
        await db.test_collection.delete_one({"_id": result.inserted_id})
        logger.info("✓ Cleaned up test document")
        
        return True
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        logger.error("Full error details:", exc_info=True)
        return False

if __name__ == "__main__":
    result = asyncio.run(test_connection())
    if not result:
        print("\nTroubleshooting steps:")
        print("1. Verify your IP is whitelisted in MongoDB Atlas")
        print("2. Check the username/password in the connection string")
        print("3. Ensure the cluster is running and accessible")
