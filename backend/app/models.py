from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID

class User(SQLModel, table=True):
    """User model for authentication and profile."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    full_name: str
    region: str = "Global"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    emissions: List["EmissionEntry"] = Relationship(back_populates="user")
    profile: Optional["UserProfile"] = Relationship(back_populates="user")


class EmissionEntry(SQLModel, table=True):
    """Carbon emission log entry."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    category: str  # "transport", "energy", "food"
    subcategory: str  # "car", "flight", "electricity", "beef", etc.
    quantity: float
    unit: str  # "km", "kWh", "meal"
    co2_equivalent: float  # Calculated CO2 in kg
    date: str  # YYYY-MM-DD format
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="emissions")


class UserProfile(SQLModel, table=True):
    """User preferences and profile settings."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", unique=True, index=True)
    household_size: int = 1
    vehicle_type: str = "car"  # "car", "electric_car", "bus", "train", "flight"
    energy_source: str = "grid"  # "grid", "renewable"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="profile")
