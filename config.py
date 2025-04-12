import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI", "")
if not MONGO_URI:
    raise ValueError("No MongoDB URI provided. Set MONGODB_URI environment variable")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "realtime-docs")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
JWT_REFRESH_EXPIRE_HOURS = 72  # 3 days
