from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from uuid import UUID

from app.database import get_session
from app.models import User
from app.schemas import RecommendationsResponse, RecommendationItem
from app.services.recommendations import get_recommendations
from app.services.auth import get_user_id_from_token

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

def get_current_user_id(request: Request) -> UUID:
    """Extract user ID from token in request scope."""
    token = request.scope.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user_id

@router.get("", response_model=RecommendationsResponse)
def get_user_recommendations(
    request: Request,
    limit: int = 5,
    session: Session = Depends(get_session),
):
    """Get personalized recommendations for reducing carbon footprint."""
    user_id = get_current_user_id(request)
    
    # Verify user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get recommendations
    recommendations, total_savings = get_recommendations(session, user_id, limit)
    
    # Convert to response schema
    rec_items = [
        RecommendationItem(
            id=rec["id"],
            category=rec["category"],
            action=rec["action"],
            description=rec["description"],
            potential_savings=rec["savings"],
            priority=rec["priority"],
            difficulty=rec["difficulty"]
        )
        for rec in recommendations
    ]
    
    return RecommendationsResponse(
        recommendations=rec_items,
        total_potential_savings=total_savings
    )
