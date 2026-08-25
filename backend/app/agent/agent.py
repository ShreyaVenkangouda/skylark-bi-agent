import json
import time

from google import genai

from app.config import settings

from app.agent.prompts import SYSTEM_PROMPT


class BusinessAgent:

    def __init__(self):

        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.models = [
            settings.GEMINI_MODEL,
            "gemini-3.6-flash",
        ]

    def answer(
        self,
        question,
        context
    ):

        prompt = f"""
{SYSTEM_PROMPT}

BUSINESS DATA:

{json.dumps(
    context,
    default=str,
    indent=2
)}

USER QUESTION:

{question}

Answer using only the supplied
business data.

Give a concise executive-level
answer.

If the data does not support a
claim, say so.
"""

        last_error = None

        for model in self.models:

            for attempt in range(2):

                try:

                    response = (
                        self.client.models.generate_content(
                            model=model,
                            contents=prompt
                        )
                    )

                    if response.text:
                        return response.text

                except Exception as exc:

                    last_error = exc

                    # Wait before retrying temporary
                    # Gemini server errors.
                    time.sleep(2)

        raise RuntimeError(
            f"Gemini API unavailable: {last_error}"
        )