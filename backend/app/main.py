from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from app.database import create_db_and_tables, settings
from app.routers import auth, emissions, profile, recommendations

# Create FastAPI app
app = FastAPI(
    title="Carbon Footprint Tracker",
    description="Track and reduce your carbon footprint",
    version="1.0.0"
)

# Security scheme
security = HTTPBearer()

# Add CORS middleware FIRST (important: add before routes and other middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Middleware to extract token from header and pass to routes
@app.middleware("http")
async def add_token_to_scope(request: Request, call_next):
    """Extract Bearer token from Authorization header and ensure CORS headers."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix
        request.scope["token"] = token
    else:
        request.scope["token"] = None
    
    response = await call_next(request)
    # Always add CORS headers to responses
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# Custom exception handler for HTTPException to ensure CORS headers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={"Access-Control-Allow-Origin": "*"}
    )

# Create tables on startup
@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup."""
    try:
        create_db_and_tables()
    except Exception as e:
        print(f"Error creating tables: {e}")

# Include routers
app.include_router(auth.router)
app.include_router(emissions.router)
app.include_router(profile.router)
app.include_router(recommendations.router)

# Override dependency for token
def get_token(request: Request) -> str:
    """Get token from request scope."""
    return request.scope.get("token")

# Root endpoint
@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Carbon Footprint Tracker API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.options("/{full_path:path}", include_in_schema=False)
async def preflight_handler(full_path: str):
    """Handle CORS preflight requests."""
    return {}

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
