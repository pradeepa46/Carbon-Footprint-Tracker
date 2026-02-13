from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime

from app.database import get_session
from app.models import User, UserProfile
from app.schemas import UserProfileUpdate, UserProfileResponse, UserResponse
from app.services.auth import get_user_id_from_token

router = APIRouter(prefix="/api/profile", tags=["profile"])

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

@router.get("", response_model=UserProfileResponse)
def get_profile(
    request: Request,
    session: Session = Depends(get_session),
):
    """Get user profile with settings."""
    user_id = get_current_user_id(request)
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get or create profile
    profile = session.exec(
        select(UserProfile).where(UserProfile.user_id == user_id)
    ).first()
    
    if not profile:
        profile = UserProfile(user_id=user_id)
        session.add(profile)
        session.commit()
        session.refresh(profile)
    
    return UserProfileResponse(
        user=UserResponse.from_orm(user),
        household_size=profile.household_size,
        vehicle_type=profile.vehicle_type,
        energy_source=profile.energy_source
    )

@router.put("", response_model=UserProfileResponse)
def update_profile(
    profile_update: UserProfileUpdate,
    request: Request,
    session: Session = Depends(get_session),
):
    """Update user profile and settings."""
    user_id = get_current_user_id(request)
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get or create profile
    profile = session.exec(
        select(UserProfile).where(UserProfile.user_id == user_id)
    ).first()
    
    if not profile:
        profile = UserProfile(user_id=user_id)
        session.add(profile)
    
    # Update user fields
    if profile_update.full_name:
        user.full_name = profile_update.full_name
    if profile_update.region:
        user.region = profile_update.region
    
    # Update profile fields
    if profile_update.household_size:
        profile.household_size = profile_update.household_size
    if profile_update.vehicle_type:
        profile.vehicle_type = profile_update.vehicle_type
    if profile_update.energy_source:
        profile.energy_source = profile_update.energy_source
    
    user.updated_at = datetime.utcnow()
    profile.updated_at = datetime.utcnow()
    
    session.add(user)
    session.add(profile)
    session.commit()
    session.refresh(user)
    session.refresh(profile)
    
    return UserProfileResponse(
        user=UserResponse.from_orm(user),
        household_size=profile.household_size,
        vehicle_type=profile.vehicle_type,
        energy_source=profile.energy_source
    )
