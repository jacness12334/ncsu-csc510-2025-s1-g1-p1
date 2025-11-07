## How to Build and Run

### Prerequisites
- Node.js 18 or higher  
- Python 3.10 or higher  
- MySQL Server  
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/jacness12334/ncsu-csc510-2025-s1-g1-p1.git
cd ncsu-csc510-2025-s1-g1-p1
```

### 2. Backend Setup (Flask)

#### Switch to backend branch and navigate to backend directory:
```bash
git checkout backend
cd proj2/backend
```

#### Set up Python environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Install Python dependencies:
```bash
pip install flask flask-sqlalchemy mysql-connector-python sqlalchemy pymysql
```

#### Database Setup:
1. Create MySQL database:
```sql
CREATE DATABASE movie_munchers_dev;
CREATE DATABASE movie_munchers_test;
CREATE DATABASE movie_munchers_prod;
```

2. The backend uses MySQL connection with these credentials (update in `app/app.py` if needed):
   - User: `root`
   - Password: `` (empty)
   - Host: `localhost`

#### Start the backend:
```bash
python -c "from app.app import get_app; app = get_app('development'); app.run(debug=True)"
```
Backend runs on `http://localhost:5000`

### 3. Frontend Setup (Next.js)

#### Switch to frontend branch and navigate to frontend directory:
```bash
git checkout frontend_skeleton
cd proj2/frontend
```

#### Install dependencies and start:
```bash
npm install
npm run dev
```
Frontend runs on `http://localhost:3000`

### 4. Run Tests
**Note**: Test configurations may need verification
Frontend:
```bash
cd proj2/frontend
npm test
```
Backend:
```bash
cd proj2/backend
pytest
```

### 5. Build for Production (Frontend only)
```bash
cd proj2/frontend
npm run build
npm start
```

### 6. Generate Documentation (Frontend)
```bash
cd proj2/frontend
npm run docs:serve
```
Documentation available at `http://localhost:3000`

## Notes
- Backend and frontend are on separate branches (`backend` and `frontend_skeleton`)
- You may need to create a `requirements.txt` file for easier dependency management
- Database migrations and initial data setup may require additional steps
