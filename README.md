# 🌱 Carbon Footprint Tracker

A comprehensive web application for tracking and reducing personal carbon emissions. Built with Vue 3, FastAPI, and PostgreSQL.

**Live Demo:** https://your-domain.vercel.app (Coming soon)  
**GitHub:** https://github.com/YOUR_USERNAME/carbon-footprint-tracker

---

## Features ✨

### 🎯 Core Functionality
- **📊 Dashboard** - Real-time CO₂ emission tracking with monthly summary and progress ring
- **➕ Emission Logging** - Easy-to-use form for tracking transport, energy, and food emissions
- **📋 History** - View, filter, and manage all logged emissions
- **📈 Analytics** - Monthly trends, breakdown charts, and yearly comparisons
- **💡 Recommendations** - AI-powered, personalized suggestions to reduce carbon footprint
- **⚙️ Profile Management** - Customize preferences and household settings

### 🎮 User Experience
- **Interactive Charts** - Animated pie charts and trend visualizations
- **Real-time Calculations** - Instant CO₂ estimates while logging
- **Gamification** - Streaks, badges, and achievement tracking
- **Mobile Responsive** - Works seamlessly on phones, tablets, and desktops
- **Dark Mode Ready** - Tailwind CSS support for light/dark themes

### 🔐 Security
- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Bcrypt encrypted passwords
- **CORS Protection** - Restricted API access
- **Input Validation** - Pydantic schemas prevent malicious data

---

## Tech Stack 🛠️

### Backend
- **FastAPI** - Modern async Python web framework
- **SQLModel** - Type-safe ORM combining SQLAlchemy and Pydantic
- **PostgreSQL** - Robust relational database
- **Uvicorn** - ASGI server for production

### Frontend
- **Vue 3** - Reactive JavaScript framework with Composition API
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Chart.js** - Beautiful data visualizations
- **Pinia** - Vue state management store

### DevOps
- **Docker** - Containerization
- **Render.com** - Backend hosting (free tier)
- **Vercel** - Frontend hosting (free tier)

---

## Getting Started 🚀

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (for local PostgreSQL)
- Git

### Local Development Setup

#### 1. Clone Repository
```powershell
# Replace YOUR_REPO_URL with your actual repository URL
git clone "https://github.com/YOUR_USERNAME/carbon-footprint-tracker.git"
cd "pradee hackathon"
```

#### 2. Setup Backend

```bash
# Create .env from template
cp backend/.env.example backend/.env

# Start PostgreSQL
docker-compose up -d

# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate
# Or (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if using Alembic)
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload
```

Server will be available at: http://localhost:8000

**API Documentation:** http://localhost:8000/docs

#### 3. Setup Frontend

```bash
# In a new terminal
cd frontend

# Create .env.local from template
cp .env.example .env.local

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## API Endpoints 📡

### Authentication
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Get JWT token
- `GET /api/auth/me` - Get current user

### Emissions
- `POST /api/emissions` - Log new emission
- `GET /api/emissions/history` - Get emission history (paginated)
- `GET /api/emissions/breakdown` - Get monthly breakdown
- `PUT /api/emissions/{id}` - Update emission
- `DELETE /api/emissions/{id}` - Delete emission

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile settings

### Recommendations
- `GET /api/recommendations` - Get personalized tips

---

## Emission Factors (Global Averages)

### Transportation (per km)
| Vehicle | CO₂ per km |
|---------|-----------|
| Car | 0.21 kg |
| Electric Car | 0.08 kg |
| Bus | 0.06 kg |
| Train | 0.04 kg |
| Flight | 0.25 kg |
| Motorcycle | 0.09 kg |

### Energy (per kWh)
- Grid Electricity: 0.385 kg CO₂
- Natural Gas: 0.20 kg CO₂
- Heating Oil: 0.268 kg CO₂

### Food (per meal/serving)
- Beef: 27 kg CO₂
- Pork: 4 kg CO₂
- Chicken: 2.5 kg CO₂
- Fish: 3.5 kg CO₂
- Dairy/Cheese: 5 kg CO₂
- Plant-based: 1 kg CO₂

---

## Deployment 🌐

### Backend Deployment (Render)

1. **Create Render Account**
   - Sign up at https://render.com

2. **Create PostgreSQL Instance**
   - New → PostgreSQL
   - Region: Choose closest to users
   - Tier: Free (512MB storage)
   - Copy database URL

3. **Deploy FastAPI Service**
   - Connect GitHub repository
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Environment Variables:
     ```
     DATABASE_URL=postgresql://user:password@host:5432/carbon_db
     JWT_SECRET_KEY=your-generated-secret-key
     JWT_ALGORITHM=HS256
     JWT_EXPIRATION_HOURS=24
     FRONTEND_URL=https://your-domain.vercel.app
     ```

### Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Sign up at https://vercel.com

2. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

3. **Deploy Frontend**
   - Connect GitHub repository
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment Variables:
     ```
     VITE_API_URL=https://your-backend.onrender.com
     ```

4. **Deploy**
   ```bash
   vercel --prod
   ```

---

## Environment Variables 🔑

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/carbon_db
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
FRONTEND_URL=http://localhost:5173
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000
```

### Generate Secure JWT Key
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## Database Schema 🗄️

### User Table
```
- id (UUID, primary key)
- email (string, unique)
- password_hash (string)
- full_name (string)
- region (string)
- created_at (datetime)
- updated_at (datetime)
```

### EmissionEntry Table
```
- id (UUID, primary key)
- user_id (UUID, foreign key)
- category (string: transport/energy/food)
- subcategory (string)
- quantity (float)
- unit (string: km/kWh/meal)
- co2_equivalent (float)
- date (string: YYYY-MM-DD)
- notes (text, optional)
- created_at (datetime)
```

### UserProfile Table
```
- id (UUID, primary key)
- user_id (UUID, foreign key)
- household_size (int)
- vehicle_type (string)
- energy_source (string)
- created_at (datetime)
- updated_at (datetime)
```

---

## Project Structure 📁

```
pradee-hackathon/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   ├── database.py             # DB setup
│   │   ├── models.py               # SQLModel schemas
│   │   ├── schemas.py              # Pydantic validators
│   │   ├── routers/
│   │   │   ├── auth.py            # Auth endpoints
│   │   │   ├── emissions.py       # Emission endpoints
│   │   │   ├── profile.py         # Profile endpoints
│   │   │   └── recommendations.py # Recommendation endpoints
│   │   └── services/
│   │       ├── auth.py            # Auth logic
│   │       ├── emissions.py       # CO2 calculations
│   │       └── recommendations.py # Recommendation engine
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.ts                # Entry point
│   │   ├── App.vue
│   │   ├── components/            # Reusable components
│   │   │   ├── Button.vue
│   │   │   ├── Card.vue
│   │   │   ├── StatCard.vue
│   │   │   ├── ProgressRing.vue
│   │   │   ├── Badge.vue
│   │   │   └── EmissionForm.vue
│   │   ├── views/                 # Page components
│   │   │   ├── Auth/
│   │   │   │   ├── Login.vue
│   │   │   │   └── Register.vue
│   │   │   ├── Dashboard.vue
│   │   │   ├── LogEmission.vue
│   │   │   ├── History.vue
│   │   │   ├── Analytics.vue
│   │   │   ├── Recommendations.vue
│   │   │   └── Profile.vue
│   │   ├── layouts/
│   │   │   └── MainLayout.vue
│   │   ├── router/
│   │   │   └── index.ts
│   │   ├── stores/
│   │   │   ├── auth.ts
│   │   │   └── emissions.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   └── styles/
│   │       └── main.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── .env.example
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Usage Guide 📖

### First Time Setup
1. Register account with email and password
2. Set household preferences (size, vehicle type, energy source)
3. Start logging emissions - click "Log Your Emission"

### Logging Emissions
1. Choose category: Transport, Energy, or Food
2. Select subcategory (e.g., "Car", "Electricity", "Beef")
3. Enter quantity and date
4. System auto-calculates CO₂ impact
5. Submit to save

### Viewing Progress
- **Dashboard**: See monthly total and breakdown
- **Analytics**: View yearly trends and comparisons
- **History**: Review all past entries with filters
- **Recommendations**: Get personalized tips based on your habits

---

## Cost Breakdown 💰

| Component | Cost | Notes |
|-----------|------|-------|
| Vercel (Frontend) | $0 | Free tier unlimited |
| Render (Backend) | $0 | Free tier with 0.5 CPU |
| SQLite (Local Dev) | $0 | Included |
| PostgreSQL (Render) | $0-5/mo | Free tier 256MB |
| Domain (Optional) | $12/year | Namecheap, etc. |
| **Total Year 1** | **$12-60** | Extremely affordable |

---

## Future Enhancements 🚀

### Phase 2
- [ ] Regional carbon intensity factors
- [ ] Advanced analytics and heatmaps
- [ ] Social leaderboards and challenges
- [ ] Data export/sharing (PDF, CSV)
- [ ] Mobile app (React Native)
- [ ] Social login (Google, GitHub)

### Phase 3
- [ ] Carbon offset marketplace integration
- [ ] AI-powered insights and predictions
- [ ] API for third-party integrations
- [ ] Multi-language support
- [ ] Advanced achievement system

---

## Contributing 🤝

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## License 📄

This project is licensed under the MIT License - see LICENSE file for details.

---

## Support 💬

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions
- **Email**: support@carbonfootprinttracker.app

---

## Acknowledgments 🙏

- GHG Protocol for emission factor standards
- Our World in Data for carbon research
- Global Footprint Network for reference data
- Vue.js, FastAPI, and open-source communities

---

**Together, we can make climate action accessible to everyone. 🌍🌱**
