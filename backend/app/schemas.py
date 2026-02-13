from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# ==================== AUTH SCHEMAS ====================

class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=2)

class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: UUID

class UserResponse(BaseModel):
    """User profile response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: str
    full_name: str
    region: str
    created_at: datetime

# ==================== EMISSION SCHEMAS ====================

class EmissionEntryCreate(BaseModel):
    """Request to create emission entry."""
    category: str  # "transport", "energy", "food"
    subcategory: str
    quantity: float
    unit: str
    date: str  # "YYYY-MM-DD"
    notes: Optional[str] = None

class EmissionEntryUpdate(BaseModel):
    """Request to update emission entry."""
    category: Optional[str] = None
    subcategory: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    date: Optional[str] = None
    notes: Optional[str] = None

class EmissionEntryResponse(BaseModel):
    """Emission entry response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    category: str
    subcategory: str
    quantity: float
    unit: str
    co2_equivalent: float
    date: str
    notes: Optional[str]
    created_at: datetime

# ==================== PROFILE SCHEMAS ====================

class UserProfileUpdate(BaseModel):
    """Request to update user profile."""
    full_name: Optional[str] = None
    region: Optional[str] = None
    household_size: Optional[int] = None
    vehicle_type: Optional[str] = None
    energy_source: Optional[str] = None

class UserProfileResponse(BaseModel):
    """User profile response with settings."""
    user: UserResponse
    household_size: int
    vehicle_type: str
    energy_source: str

# ==================== ANALYTICS SCHEMAS ====================

class EmissionBreakdown(BaseModel):
    """Breakdown of emissions by category."""
    transport: float
    energy: float
    food: float
    total: float

class EmissionBreakdownResponse(BaseModel):
    """Analytics response for period."""
    period: str  # "month" or "week"
    year: int
    month: int
    day: Optional[int] = None
    summary: dict  # Contains total_co2_kg, daily_average, trend
    breakdown: EmissionBreakdown
    entries: List[EmissionEntryResponse]

class RecommendationItem(BaseModel):
    """Single recommendation."""
    id: str
    category: str
    action: str
    description: str
    potential_savings: float  # kg CO2
    priority: str  # "high", "medium", "low"
    difficulty: str  # "easy", "medium", "hard"

class RecommendationsResponse(BaseModel):
    """Personalized recommendations response."""
    recommendations: List[RecommendationItem]
    total_potential_savings: float
