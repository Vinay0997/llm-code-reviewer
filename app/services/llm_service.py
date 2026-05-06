from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.models.schemas import CodeReviewResponse
from app.core.config import settings
import json

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=settings.OPENAI_API_KEY,
    temperature=0.2
)

REVIEW_PROMPT = """
You are an expert code reviewer. Analyze the following {language} code and return a detailed review.

Context: {context}

Code:
```{language}
{code}
```

Respond ONLY with a valid JSON object matching this schema:
{
  "summary": "Brief overview of code quality",
  "issues": [
    {
      "type": "bug|security|style|optimization",
      "severity": "low|medium|high",
      "line": "line number or range if known",
      "description": "what the issue is",
      "suggestion": "how to fix it"
    }
  ],
  "score": <integer 0-100>,
  "improved_code": "optional refactored version"
}
"""

prompt = ChatPromptTemplate.from_template(REVIEW_PROMPT)

async def review_code(code: str, language: str, context: str) -> CodeReviewResponse:
    chain = prompt | llm
    result = await chain.ainvoke({
        "code": code,
        "language": language,
        "context": context or "No additional context provided."
    })
    raw = result.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    data = json.loads(raw)
    return CodeReviewResponse(**data)
