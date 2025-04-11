import asyncio
from db.mongo import get_db
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_document_operations():
    try:
        db = get_db()
        test_id = "direct-test-doc"
        
        # Test insert
        logger.info("Testing document insert...")
        insert_result = await db.documents.insert_one({
            "doc_id": test_id,
            "content": "Test content",
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow()
        })
        logger.info(f"Insert result: {insert_result.inserted_id}")

        # Test find
        logger.info("Testing document find...")
        doc = await db.documents.find_one({"doc_id": test_id})
        logger.info(f"Found document: {doc}")

        # Test update
        logger.info("Testing document update...")
        update_result = await db.documents.update_one(
            {"doc_id": test_id},
            {"$set": {"content": "Updated content"}}
        )
        logger.info(f"Update result: {update_result.raw_result}")

        # Verify update
        updated_doc = await db.documents.find_one({"doc_id": test_id})
        logger.info(f"Updated document content: {updated_doc['content']}")

        # Cleanup
        await db.documents.delete_one({"doc_id": test_id})
        return True
        
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    result = asyncio.get_event_loop().run_until_complete(test_document_operations())
    print(f"\nTest {'passed' if result else 'failed'}")
    exit(0 if result else 1)
