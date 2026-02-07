import json
import os
from typing import Any

from openai import OpenAI

DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


class AIServiceError(RuntimeError):
    pass


def _client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise AIServiceError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def _safe_json(text: str) -> dict[str, Any]:
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return {}
    return {}


def interpret_and_extract(narrative: str) -> dict[str, Any]:
    instructions = (
        "You are NightCipher, a dream interpretation assistant. "
        "Return JSON only, no markdown. "
        "Schema: {"
        '"title": str, '
        '"psych_summary": str, '
        '"spiritual_summary": str, '
        '"tags": [str], '
        '"symbols": [str], '
        '"emotions": [str], '
        '"people": [str], '
        '"settings": [str], '
        '"followup_question": str'
        "}. Keep summaries under 120 words each."
    )
    response = _client().responses.create(
        model=DEFAULT_MODEL,
        input=narrative,
        instructions=instructions,
    )
    data = _safe_json(getattr(response, "output_text", ""))
    return data or {}


def dream_chat_reply(narrative: str, history: list[dict[str, str]], message: str) -> str:
    instructions = (
        "You are NightCipher, a calm, professional dream companion. "
        "Ask gentle questions and reflect both psychological and spiritual angles. "
        "Keep replies under 120 words."
    )
    input_messages = [
        {"role": "system", "content": f"Dream narrative: {narrative}"},
        *history,
        {"role": "user", "content": message},
    ]
    response = _client().responses.create(
        model=DEFAULT_MODEL,
        input=input_messages,
        instructions=instructions,
    )
    return (getattr(response, "output_text", "") or "").strip()
