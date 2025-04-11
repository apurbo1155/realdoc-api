import asyncio
from db.dependencies import get_db, get_mongo_client

async def test_connection():
    client = None
    try:
        # First test direct client connection
        client = await get_mongo_client()
        print("MongoDB client connection successful")
        
        # Then test database operations
        db = await get_db(client)
        ping_result = await db.command('ping')
        print(f"MongoDB ping successful: {ping_result}")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")
        return False
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
