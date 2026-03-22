"""System and informational endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint with API information and route summary."""

    return {
        "message": "JWT Authentication API with Memory Integration",
        "endpoints": {
            "signup": "POST /signup - Register new user (username, email, password)",
            "login": "POST /login - Authenticate user and get JWT token",
            "chat": "POST /chat - Send a message to AI",
            "generate_question": "POST /generate-question - Generate next batch of 2 MCQs with explanations",
            "protected": "GET /protected - Access protected route with token",
            "profile": "GET /user/profile - Get user profile",
            "store_memory": "POST /store-memory - Store quiz attempt in memory",
            "store_memory_batch": "POST /store-memory-batch - Store 2 quiz attempts in memory",
            "weak_topics": "GET /weak-topics/{user_id} - Get topics with score < 50",
            "mistakes": "GET /mistakes/{user_id} - Get list of past mistakes",
            "insights": "GET /insights/{user_id} - Get comprehensive learning insights",
            "docs": "GET /docs - Interactive API documentation",
        },
        "test_credentials": {"username": "user1", "password": "password123"},
        "signup_example": {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "mypassword123",
        },
        "memory_example": {
            "user_id": "user1",
            "topic": "Algebra",
            "mistake_type": "Conceptual",
            "difficulty": "Medium",
            "score": 75,
        },
    }
