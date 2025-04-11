import asyncio
from db.mongo import get_db

async def test_connection():
    try:
        db = get_db()
        result = await db.command('ping')
        print("Connection successful:", result)
    except Exception as e:
        print("Connection failed:", str(e))

asyncio.run(test_connection())
