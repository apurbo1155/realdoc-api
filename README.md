# Real-time Collaborative Document API (realdoc-api)

Backend API for the real-time collaborative document editor, handling:
- WebSocket connections for real-time collaboration
- Document persistence and versioning
- User authentication and authorization
- Operational transform conflict resolution

## Features

- FastAPI-based REST API
- WebSocket endpoints for real-time updates
- JWT authentication
- MongoDB document storage
- Automatic conflict resolution
- Crash recovery system

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables (copy .env.example to .env)
5. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

## Environment Variables

Required variables in `.env`:
```
MONGODB_URI=mongodb_connection_string
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Documentation

After running the server:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment

1. Push to GitHub repository
2. Deploy to Render/Heroku with:
   - PORT environment variable set to 8000
   - MongoDB connection string configured
   - JWT secret set
