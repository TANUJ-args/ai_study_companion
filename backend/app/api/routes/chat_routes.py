"""Chat and quiz generation endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.chat import ChatRequest
from app.schemas.quiz import GenerateQuestionRequest, GenerateQuestionResponse
from app.services.llm_service import ask_llm, generate_quiz_questions

router = APIRouter()


@router.post("/chat", response_model=dict)
async def chat_with_ai(chat_request: ChatRequest):
    """Forward a user message to the configured LLM provider."""

    if not chat_request.message or not chat_request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty",
        )

    try:
        reply = ask_llm(chat_request.message.strip())
        return {"reply": reply}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to get response from AI provider",
        )


@router.post("/generate-question", response_model=GenerateQuestionResponse)
async def generate_question(payload: GenerateQuestionRequest):
    """Generate two MCQs for a given topic and difficulty."""

    try:
        question_data = generate_quiz_questions(
            topic=payload.topic.strip(),
            difficulty=payload.difficulty,
            count=payload.question_count,
        )
        return GenerateQuestionResponse.model_validate(
            {
                "topic": payload.topic.strip(),
                "difficulty": payload.difficulty,
                "batch_size": payload.question_count,
                "questions": question_data.get("questions", []),
            }
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {exc}",
        ) from exc
