from fastapi import APIRouter, HTTPException, Request, Depends
import json
from pydantic import BaseModel
from typing import Dict
import logging
import datetime
from db.dependencies import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class DocumentContent(BaseModel):
    content: str

@router.post("/auth/signup")
async def signup(user: UserCreate, request: Request, db=Depends(get_db)):
    logger.info(f"Signup attempt for username: {user.username}")
    logger.info(f"Request headers: {request.headers}")
    logger.info(f"Origin header: {request.headers.get('origin')}")
    
    # Basic validation
    if not all([user.username, user.password, user.email]):
        logger.error("Missing required fields")
        raise HTTPException(status_code=422, detail="All fields are required")
    
    # Check if username exists
    existing_user = await db.users.find_one({"username": user.username})
    if existing_user:
        logger.warning(f"Username already exists: {user.username}")
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "Username already exists",
                "suggestion": "Please choose a different username"
            }
        )

    # Hash password before storing
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user.password)

    # Create new user
    new_user = {
        "username": user.username,
        "password": hashed_password,
        "email": user.email,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    }

    try:
        result = await db.users.insert_one(new_user)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        return {
            "message": "User created successfully",
            "username": user.username,
            "email": user.email
        }
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/auth/login")
async def login(user: UserLogin, db=Depends(get_db)):
    logger.info(f"Login attempt for username: {user.username}")
    
    if not all([user.username, user.password]):
        raise HTTPException(status_code=422, detail="Username and password are required")

    existing_user = await db.users.find_one({"username": user.username})
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    if not pwd_context.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    from auth.jwt_handler import create_access_token
    from config import ACCESS_TOKEN_EXPIRE_MINUTES
    
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {
        "message": "Login successful",
        "username": user.username,
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get("/documents/{doc_id}")
async def get_document(doc_id: str, db=Depends(get_db)):
    try:
        logger.info(f"Attempting to load document: {doc_id}")
        # Verify collection exists
        if 'documents' not in (await db.list_collection_names()):
            logger.error("Documents collection does not exist")
            await db.create_collection('documents')
            
        document = await db.documents.find_one({"doc_id": doc_id})
        
        if not document:
            logger.info(f"Document {doc_id} not found, creating new one")
            try:
                result = await db.documents.insert_one({
                    "doc_id": doc_id,
                    "content": "",
                    "created_at": datetime.datetime.utcnow(),
                    "updated_at": datetime.datetime.utcnow()
                })
                if not result.inserted_id:
                    logger.error("Failed to create new document")
                    raise HTTPException(status_code=500, detail="Failed to create document")
                logger.info(f"Created new document with ID: {result.inserted_id}")
                return {"content": ""}
            except Exception as e:
                logger.error(f"Error creating document: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error creating document: {str(e)}")
        
        logger.info(f"Successfully loaded document: {doc_id}")
        return {"content": document.get("content", "")}
    except Exception as e:
        logger.error(f"Error getting document {doc_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error loading document: {str(e)}")

from api.websocket import manager as ws_manager

@router.post("/documents/{doc_id}")
async def save_document(doc_id: str, document: DocumentContent, request: Request, db=Depends(get_db)):
    try:
        logger.info(f"Attempting to save document: {doc_id}")
        
        # Verify database connection by attempting a simple operation
        try:
            await db.command('ping')
        except Exception as e:
            logger.error(f"Database connection verification failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Database connection verification failed")
        
        # Verify collection exists
        collections = await db.list_collection_names()
        logger.debug(f"Available collections: {collections}")
        
        if 'documents' not in collections:
            logger.info("Creating documents collection")
            try:
                await db.create_collection('documents')
                logger.info("Successfully created documents collection")
            except Exception as create_error:
                logger.error(f"Failed to create collection: {str(create_error)}", exc_info=True)
                raise HTTPException(status_code=500, detail="Failed to create collection")
        
        # Save to database with detailed logging
        logger.debug(f"Saving document content: {document.content}")
        result = await db.documents.update_one(
            {"doc_id": doc_id},
            {"$set": {
                "content": document.content,
                "updated_at": datetime.datetime.utcnow()
            }},
            upsert=True
        )
        
        # Detailed result analysis
        logger.debug(f"Update result: {result.raw_result}")
        if not result.acknowledged:
            logger.error("Document save not acknowledged by database")
            raise HTTPException(status_code=500, detail="Document save not acknowledged by database")
            
        if result.matched_count == 0 and result.upserted_id is None:
            logger.error("Document was neither matched nor upserted")
            raise HTTPException(status_code=500, detail="Document save failed")
        
        logger.info(f"Successfully saved document: {doc_id}. Matched: {result.matched_count}, Modified: {result.modified_count}, Upserted ID: {result.upserted_id}")
        
        # Broadcast update to all connected clients
        await ws_manager.broadcast(
            json.dumps({
                "type": "content_update",
                "content": document.content
            }),
            doc_id
        )
        
        return {"message": "Document saved successfully"}
    except Exception as e:
        logger.error(f"Error saving document {doc_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error saving document: {str(e)}")