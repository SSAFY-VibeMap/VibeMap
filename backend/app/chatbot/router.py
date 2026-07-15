from fastapi import APIRouter

from app.chatbot.schemas import ChatRequest, ChatResponse
from app.chatbot.service import ChatService

router = APIRouter(prefix="/api/chat", tags=["chatbot"])
chat_service = ChatService()


@router.post("", response_model=ChatResponse)
def send_chat_message(request: ChatRequest) -> ChatResponse:
    return chat_service.generate_reply(request)