import os
from dotenv import load_dotenv

load_dotenv()

print("MONGO_URI:", os.getenv("MONGO_URI"))
