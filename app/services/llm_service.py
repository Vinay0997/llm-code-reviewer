from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.models.schemas import CodeReviewResponse
from app.core.config import settings
import json

_persistent_llm = None

def get_llm():
    global _persistent_llm
    if _persistent_llm is None:
        _persistent_llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.5-flash",
            api_key=settings.GOOGLE_API_KEY,
            temperature=0.2,
            convert_system_message_to_human=True
        )
    return _persistent_llm

REVIEW_PROMPT = """
You are an expert code reviewer. Analyze the following {language} code and return a detailed review.
Context: {context}
Code:
```{language}
{code}
```
Respond ONLY with a valid JSON object matching this schema:
{
  "{{summary}}": "Brief overview of code quality",
  "{{issues}}": [
    {
      "{{type}}": "bug|security|style|optimization",
      "{{severity}}": "low|medium|high",
      "{{line}}": "line number or range if known",
      "{{description}}": "what the issue is",
      "{{suggestion}}": "how to fix it"
    }
  ],
  "{{score}}": <integer 0-100>,
  "{{improved_code}}": "optional refactored version"
}
"""

prompt = ChatPromptTemplate.from_template(REVIEW_PROMPT)

async def review_code(code: str, language: str, context: str) -> CodeReviewResponse:
    if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "":
        raise ValueError("GOOGLE_API_KEY is not set. Please set it in your .env file.")
    chain = prompt | get_llm()
    result = await chain.ainvoke({
        "code": code,
        "language": language,
        "context": context or "No additional context provided."
    })
    raw = result.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
    data = json.loads(raw)
    return CodeReviewResponse(**data)
