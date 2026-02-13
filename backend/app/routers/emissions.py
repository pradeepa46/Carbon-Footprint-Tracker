from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from uuid import UUID

from app.database import get_session
from app.models import EmissionEntry, User
from app.schemas import EmissionEntryCreate, EmissionEntryResponse, EmissionEntryUpdate, EmissionBreakdownResponse, EmissionBreakdown
from app.services.emissions import calculate_emissions
from app.services.auth import get_user_id_from_token

router = APIRouter(prefix="/api/emissions", tags=["emissions"])

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

@router.post("", response_model=EmissionEntryResponse)
def create_emission(
    emission: EmissionEntryCreate,
    request: Request,
    session: Session = Depends(get_session),
):
    """Log a new emission entry."""
    user_id = get_current_user_id(request)
    
    # Verify user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validate date format
    try:
        datetime.strptime(emission.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    # Calculate CO2 emissions
    try:
        co2_equivalent = calculate_emissions(
            emission.category,
            emission.subcategory,
            emission.quantity,
            emission.unit
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Create entry
    entry = EmissionEntry(
        user_id=user_id,
        category=emission.category,
        subcategory=emission.subcategory,
        quantity=emission.quantity,
        unit=emission.unit,
        co2_equivalent=co2_equivalent,
        date=emission.date,
        notes=emission.notes
    )
    
    session.add(entry)
    session.commit()
    session.refresh(entry)
    
    return entry

@router.get("/history", response_model=List[EmissionEntryResponse])
def get_history(
    request: Request,
    skip: int = 0,
    limit: int = 50,
    category: str = None,
    session: Session = Depends(get_session),
):
    """Get user's emission history with optional filtering."""
    user_id = get_current_user_id(request)
    
    query = select(EmissionEntry).where(EmissionEntry.user_id == user_id)
    
    if category:
        query = query.where(EmissionEntry.category == category.lower())
    
    query = query.order_by(EmissionEntry.date.desc()).offset(skip).limit(limit)
    entries = session.exec(query).all()
    
    return entries

@router.get("/breakdown", response_model=EmissionBreakdownResponse)
def get_breakdown(
    request: Request,
    year: int = None,
    month: int = None,
    session: Session = Depends(get_session),
):
    """Get emission breakdown for a given month."""
    user_id = get_current_user_id(request)
    
    if year is None or month is None:
        now = datetime.utcnow()
        year = year or now.year
        month = month or now.month
    
    # Build date filter
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be between 1 and 12"
        )
    
    # Get all entries for the month
    query = select(EmissionEntry).where(
        (EmissionEntry.user_id == user_id) &
        (EmissionEntry.date.like(f"{year:04d}-{month:02d}%"))
    )
    entries = session.exec(query).all()
    
    # Calculate breakdown
    breakdown = {
        "transport": 0,
        "energy": 0,
        "food": 0,
        "total": 0
    }
    
    for entry in entries:
        # Only count recognized categories
        if entry.category in breakdown:
            breakdown[entry.category] += entry.co2_equivalent
    
    breakdown["total"] = sum([breakdown["transport"], breakdown["energy"], breakdown["food"]])
    
    # Calculate daily average
    daily_average = breakdown["total"] / (len(set(e.date for e in entries)) or 1)
    
    return EmissionBreakdownResponse(
        period="month",
        year=year,
        month=month,
        summary={
            "total_co2_kg": round(breakdown["total"], 2),
            "daily_average": round(daily_average, 2),
            "trend": 0.0  # TODO: calculate trend vs previous month
        },
        breakdown=EmissionBreakdown(**{k: round(v, 2) for k, v in breakdown.items()}),
        entries=[EmissionEntryResponse.from_orm(e) for e in entries]
    )

@router.put("/{entry_id}", response_model=EmissionEntryResponse)
def update_emission(
    entry_id: str,
    emission: EmissionEntryUpdate,
    request: Request,
    session: Session = Depends(get_session),
):
    """Update an emission entry."""
    user_id = get_current_user_id(request)
    
    entry = session.get(EmissionEntry, UUID(entry_id))
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emission entry not found"
        )
    
    if entry.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this entry"
        )
    
    # Update fields
    if emission.category:
        entry.category = emission.category
    if emission.subcategory:
        entry.subcategory = emission.subcategory
    if emission.quantity:
        entry.quantity = emission.quantity
    if emission.unit:
        entry.unit = emission.unit
    if emission.date:
        entry.date = emission.date
    if emission.notes is not None:
        entry.notes = emission.notes
    
    # Recalculate CO2 if needed
    if emission.quantity or emission.subcategory or emission.category:
        try:
            entry.co2_equivalent = calculate_emissions(
                entry.category,
                entry.subcategory,
                entry.quantity,
                entry.unit
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    session.add(entry)
    session.commit()
    session.refresh(entry)
    
    return entry

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_emission(
    entry_id: str,
    request: Request,
    session: Session = Depends(get_session),
):
    """Delete an emission entry."""
    user_id = get_current_user_id(request)
    
    entry = session.get(EmissionEntry, UUID(entry_id))
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emission entry not found"
        )
    
    if entry.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this entry"
        )
    
    session.delete(entry)
    session.commit()
    return None
