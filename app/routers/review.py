from fastapi import APIRouter, Depends
from app.models.schemas import CodeReviewRequest, CodeReviewResponse
from app.services.llm_service import review_code
from app.auth.jwt_handler import verify_token

router = APIRouter(prefix="/api/v1", tags=["Code Review"])

@router.post("/review", response_model=CodeReviewResponse)
async def submit_review(
    request: CodeReviewRequest,
    token: dict = Depends(verify_token)
):
    return await review_code(request.code, request.language, request.context)
