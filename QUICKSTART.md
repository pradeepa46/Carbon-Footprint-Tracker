# Quick Start Guide ⚡

Get the Carbon Footprint Tracker up and running in 5 minutes!

## Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

---

## Local Setup (Windows PowerShell)

### Step 1: Clone & Navigate
```powershell
cd "c:\Users\E7490\Desktop\pradee hackathon"
```

### Step 2: Start PostgreSQL
```powershell
docker-compose up -d
# Wait ~10 seconds for database to be ready
Timeout /T 10 /NOBREAK
```

### Step 3: Setup Backend (Terminal 1)

```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit .env
Copy-Item .env.example .env

# Run backend
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000/docs

### Step 4: Setup Frontend (Terminal 2)

```powershell
cd frontend

# Install dependencies
npm install

# Copy and edit .env
Copy-Item .env.example .env.local

# Run development server
npm run dev
```

✅ Frontend running at: http://localhost:5173

---

## Testing the Application

### 1. Open http://localhost:5173 in your browser

### 2. Create Account
- Email: `test@example.com`
- Password: `password123`
- Full Name: `Test User`

### 3. Log Emissions
- Click "Log Your Emission"
- Select category (Transport)
- Choose vehicle (Car)
- Enter distance (e.g., 50 km)
- Submit

### 4. View Results
- **Dashboard**: See CO₂ summary and breakdown
- **History**: View logged emissions
- **Analytics**: See trends
- **Recommendations**: Get personalized tips
- **Profile**: Update preferences

---

## API Testing

Open http://localhost:8000/docs to test all API endpoints with Swagger UI:

1. **POST /api/auth/register** - Create account
2. **POST /api/auth/login** - Get JWT token
3. **POST /api/emissions** - Log emission
4. **GET /api/emissions/history** - View history
5. **GET /api/emissions/breakdown** - Get monthly breakdown
6. **GET /api/recommendations** - Get tips

---

## Common Issues & Solutions

### Port 5432 (PostgreSQL) Already in Use
```powershell
# Stop the conflicting container
docker ps
docker stop <container-id>
```

### Node Modules Not Installing
```powershell
# Clear cache and reinstall
rm -r node_modules
npm cache clean --force
npm install
```

### Python Virtual Environment Not Activating
```powershell
# On Windows, try:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Database Connection Error
```powershell
# Check if Postgres is running
docker ps

# Restart if needed
docker-compose restart postgres
```

---

## Project Structure

```
frontend/
├── src/components/    # Reusable UI components
├── src/views/         # Page components
├── src/stores/        # Pinia state management
├── src/services/      # API client
└── src/styles/        # Tailwind CSS

backend/
├── app/models.py      # Database schemas
├── app/schemas.py     # Validation schemas
├── app/routers/       # API endpoints
├── app/services/      # Business logic
└── app/main.py        # FastAPI app
```

---

## What's Next?

After local setup, you can:

1. **Explore the code** - Review Vue components and FastAPI routers
2. **Customize** - Change colors in `tailwind.config.js`, emission factors in `services/emissions.py`
3. **Add features** - See CONTRIBUTING.md for guidelines
4. **Deploy** - Follow `README.md` for Render + Vercel deployment

---

## Useful Commands

### Backend
```powershell
# Run tests
pytest backend/tests/

# Format code
black backend/

# Check types
mypy backend/
```

### Frontend
```powershell
# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

---

## Database Reset

If you need to start fresh:

```powershell
# Stop and remove containers
docker-compose down -v

# Remove backend virtual environment
rm -r backend\venv

# Then repeat setup steps above
```

---

**Happy tracking! 🌱**

For detailed documentation, see README.md
