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
```bash
cd backend
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:
```
DATABASE_URL=mysql+pymysql://<user>:<password>@localhost/moviemunchers
FLASK_ENV=development
```

Start the backend:
```bash
flask run
```
Backend runs on `http://localhost:5000`

### 3. Frontend Setup (Next.js)
```bash
cd ../frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:3000`

### 4. Run Tests
Frontend:
```bash
npm test
```
Backend:
```bash
pytest
```

### 5. Build for Production (optional)
```bash
npm run build
npm start
```
