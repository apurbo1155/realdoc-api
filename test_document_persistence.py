import requests
import datetime

def test_document_operations():
    # Create unique test document ID
    doc_id = f"test-doc-{datetime.datetime.now().timestamp()}"
    test_content = f"Test content {datetime.datetime.now()}"
    
    print(f"\nTesting document persistence for ID: {doc_id}")
    
    # Test saving document
    print("\n[1] Saving document...")
    save_response = requests.post(
        f"http://localhost:8000/api/documents/{doc_id}",
        json={"content": test_content}
    )
    print(f"Save response: {save_response.status_code} - {save_response.text}")
    
    # Test loading document
    print("\n[2] Loading document...")
    load_response = requests.get(
        f"http://localhost:8000/api/documents/{doc_id}"
    )
    print(f"Load response: {load_response.status_code} - {load_response.text}")
    
    # Verify content matches
    if load_response.status_code == 200 and load_response.json().get("content") == test_content:
        print("\n✅ Persistence test PASSED - Content matches!")
        return True
    else:
        print("\n❌ Persistence test FAILED - Content mismatch!")
        return False

if __name__ == "__main__":
    test_document_operations()
