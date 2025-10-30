#!/bin/bash

echo "🚀 Setting up EcoMSME AI Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Django Settings
SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=ecomsme
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000/api
EOF
    echo "✅ .env file created!"
fi

# Setup Backend
echo "🐍 Setting up Django Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install spaCy model
echo "🤖 Installing spaCy model..."
python -m spacy download en_core_web_sm

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@ecomsme.ai

# Setup Frontend
echo "⚛️ Setting up React Frontend..."
cd ../frontend

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo "✅ Setup completed successfully!"
echo ""
echo "🎉 EcoMSME AI Platform is ready!"
echo ""
echo "To start the application:"
echo "1. Backend: cd backend && source venv/bin/activate && python manage.py runserver"
echo "2. Frontend: cd frontend && npm start"
echo "3. Or use Docker: docker-compose up -d"
echo ""
echo "🌐 Access the application at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/api"
echo "   Admin Panel: http://localhost:8000/admin"
echo ""
echo "🔑 Default admin credentials:"
echo "   Username: admin"
echo "   Email: admin@ecomsme.ai"
echo "   Password: (you'll be prompted to set this)" 