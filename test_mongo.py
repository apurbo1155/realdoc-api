import asyncio
from db.mongo import get_db

async def test_connection():
    try:
        result = await get_db().command('ping')
        print("MongoDB connection successful:", result)
        return True
    except Exception as e:
        print("MongoDB connection failed:", str(e))
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
