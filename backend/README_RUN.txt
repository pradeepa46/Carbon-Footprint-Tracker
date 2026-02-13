
# Carbon Footprint Tracker Backend — Fixed Version

## Setup (Windows / Linux / Mac)

### 1. Create virtual environment
python -m venv venv

### 2. Activate
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure environment
Copy:
.env.example → .env

Edit values if needed.

### 5. Run server
uvicorn app.main:app --reload

API Docs:
http://localhost:8000/docs
