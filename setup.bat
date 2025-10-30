@echo off
echo 🚀 Setting up EcoMSME AI Platform...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file...
    (
        echo # Django Settings
        echo SECRET_KEY=django-insecure-change-me-in-production
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo.
        echo # Database Configuration
        echo DB_NAME=ecomsme
        echo DB_USER=postgres
        echo DB_PASSWORD=postgres
        echo DB_HOST=localhost
        echo DB_PORT=5432
        echo.
        echo # Redis Configuration
        echo REDIS_URL=redis://localhost:6379/0
        echo.
        echo # JWT Settings
        echo JWT_SECRET_KEY=your-jwt-secret-key
        echo.
        echo # Frontend Configuration
        echo REACT_APP_API_URL=http://localhost:8000/api
    ) > .env
    echo ✅ .env file created!
)

REM Setup Backend
echo 🐍 Setting up Django Backend...
cd backend

REM Create virtual environment
if not exist venv (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Install spaCy model
echo 🤖 Installing spaCy model...
python -m spacy download en_core_web_sm

REM Run migrations
echo 🗄️ Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo 👤 Creating superuser...
python manage.py createsuperuser --noinput --username admin --email admin@ecomsme.ai

REM Setup Frontend
echo ⚛️ Setting up React Frontend...
cd ..\frontend

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
npm install

echo ✅ Setup completed successfully!
echo.
echo 🎉 EcoMSME AI Platform is ready!
echo.
echo To start the application:
echo 1. Backend: cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
echo 2. Frontend: cd frontend ^&^& npm start
echo 3. Or use Docker: docker-compose up -d
echo.
echo 🌐 Access the application at:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000/api
echo    Admin Panel: http://localhost:8000/admin
echo.
echo 🔑 Default admin credentials:
echo    Username: admin
echo    Email: admin@ecomsme.ai
echo    Password: ^(you'll be prompted to set this^)
pause 