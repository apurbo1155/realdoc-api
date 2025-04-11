import requests
import datetime

BASE_URL = "http://localhost:8000/api"  # Added /api prefix to match route mounting
TEST_DOC_ID = "persistence-test-doc"

def test_document_persistence():
    print(f"\nTesting document persistence for ID: {TEST_DOC_ID}")
    
    # [1] Save document
    print("[1] Saving document...")
    try:
        response = requests.post(
            f"{BASE_URL}/documents/{TEST_DOC_ID}",
            json={"content": f"Test content {datetime.datetime.now()}"}
        )
        if response.status_code != 200:
            print(f"Save failed: {response.status_code} - {response.text}")
            return False
        print("Save successful")
    
        # [2] Load document
        print("[2] Loading document...")
        response = requests.get(f"{BASE_URL}/documents/{TEST_DOC_ID}")
        if response.status_code != 200:
            print(f"Load failed: {response.status_code} - {response.text}")
            return False
        print(f"Loaded content: {response.json()['content']}")
        return True
    
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_document_persistence()
    exit(0 if success else 1)
