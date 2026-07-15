from uuid import uuid4

from fastapi import HTTPException

from backend.app.chatbot.openai_service import OpenAIService
from backend.app.chatbot.schemas import ChatRequest, ChatResponse


class ChatService:
    def __init__(self, openai_service: OpenAIService | None = None) -> None:
        self.openai_service = openai_service or OpenAIService()

    def generate_reply(self, request: ChatRequest) -> ChatResponse:
        try:
            reply = self.openai_service.generate_response(request.message, request.region)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        return ChatResponse(
            id=uuid4().hex,
            reply=reply,
        )