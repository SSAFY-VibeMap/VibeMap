from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


class OpenAIService:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate_response(self, message: str, region: str | None = None) -> str:
        if self.client is None:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        system_prompt = (
            "You are the VibeMap chatbot. Answer in Korean, keep responses concise, "
            "and help with local festivals, community posts, and nearby recommendations."
        )
        if region:
            user_prompt = f"지역: {region}\n질문: {message}"
        else:
            user_prompt = message

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except OpenAIError as exc:
            raise RuntimeError(f"OpenAI request failed: {exc}") from exc

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("OpenAI returned an empty response")

        return content.strip()
