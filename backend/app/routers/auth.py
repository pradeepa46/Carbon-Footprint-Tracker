from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest, session: Session = Depends(get_session)):
    """Register a new user."""
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == request.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        email=request.email,
        full_name=request.full_name,
        password_hash=hash_password(request.password),
        region="Global"
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    """Login user and return JWT token."""
    # Find user by email
    user = session.exec(
        select(User).where(User.email == request.email)
    ).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate JWT token
    access_token = create_access_token(user.id, user.email)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id
    )

@router.get("/me", response_model=UserResponse)
def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
):
    """Get current authenticated user profile."""
    from app.services.auth import get_user_id_from_token
    
    # Get token from request scope (set by middleware)
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
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
