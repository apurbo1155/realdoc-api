import os
import sys
import asyncio
import aiohttp
import datetime

BASE_URL = "http://localhost:8000"
TEST_DOC_ID = "persistence-test-doc"  # Fixed test document ID

async def test_document_persistence():
    print(f"\nTesting document persistence for ID: {TEST_DOC_ID}")
    
    async with aiohttp.ClientSession() as session:
        # [1] Save document
        print("[1] Saving document...")
        try:
            async with session.post(
                f"{BASE_URL}/documents/{TEST_DOC_ID}",
                json={"content": f"Test content {datetime.datetime.now()}"}
            ) as response:
                if response.status != 200:
                    print(f"Save failed: {response.status} - {await response.text()}")
                    return False
                print("Save successful")
        
            # [2] Load document
            print("[2] Loading document...")
            async with session.get(f"{BASE_URL}/documents/{TEST_DOC_ID}") as response:
                if response.status != 200:
                    print(f"Load failed: {response.status} - {await response.text()}")
                    return False
                data = await response.json()
                print(f"Loaded content: {data['content']}")
                return True
        
        except Exception as e:
            print(f"Error during test: {str(e)}")
            return False

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(test_document_persistence())
    sys.exit(0 if success else 1)
