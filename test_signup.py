import asyncio
import requests
from db.mongo import get_db
from passlib.context import CryptContext

async def test_signup():
    # Test user data
    test_user = {
        'username': 'testuser',
        'password': 'testpass',
        'email': 'test@test.com'
    }

    # Hash password
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    hashed_pw = pwd_context.hash(test_user['password'])
    test_user['password'] = hashed_pw

    # Make signup request
    response = requests.post('http://localhost:8000/api/signup', json=test_user)
    print("Signup Response:", response.text)

    # Verify in database
    db = get_db()
    user = await db.users.find_one({'username': test_user['username']})
    print("Database Record:", bool(user))

if __name__ == "__main__":
    asyncio.run(test_signup())
