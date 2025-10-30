# 🚀 EcoMSME AI - Quick Start Guide

Welcome to EcoMSME AI! This guide will help you get the platform up and running in minutes.

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

- **Docker & Docker Compose** - For containerized deployment
- **Node.js** (v16+) - For the React frontend
- **Python** (v3.9+) - For the Django backend
- **PostgreSQL** (optional, SQLite is used by default in development)

## 🎯 Quick Setup Options

### Option 1: Automated Setup (Recommended)

#### Windows
```bash
setup.bat
```

#### macOS/Linux
```bash
./setup.sh
```

### Option 2: Manual Setup

#### 1. Clone and Navigate
```bash
git clone <repository-url>
cd EcoMSME
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python manage.py migrate
python manage.py createsuperuser
```

#### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

## 🚀 Starting the Application

### Development Mode

#### Start Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python manage.py runserver
```

#### Start Frontend (in a new terminal)
```bash
cd frontend
npm start
```

### Production Mode (Docker)

```bash
docker-compose up -d
```

## 🌐 Access Points

Once running, you can access:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs

## 🔑 Default Credentials

- **Username**: admin
- **Email**: admin@ecomsme.ai
- **Password**: (set during setup)

## 📱 First Steps

1. **Register/Login**: Create your account or sign in
2. **Complete Profile**: Add your company information
3. **Upload Invoice**: Start by uploading your first invoice
4. **View Analytics**: Check your carbon footprint dashboard
5. **Get Recommendations**: Explore AI-powered suggestions

## 🛠️ Key Features to Try

### 📄 Invoice Upload
- Upload PDF, image, or text files
- AI automatically extracts environmental data
- View processing results and carbon impact

### 📊 Carbon Score Dashboard
- Real-time carbon footprint tracking
- Material and supplier breakdowns
- Historical trends and comparisons

### 🤖 AI Suggestions
- Personalized sustainability recommendations
- Material substitution suggestions
- Cost-benefit analysis

### 🧮 What-if Simulator
- Simulate different material choices
- Compare environmental impacts
- Plan sustainability improvements

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=ecomsme
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Frontend
REACT_APP_API_URL=http://localhost:8000/api
```

### Database Configuration

By default, the application uses SQLite for development. For production:

1. Install PostgreSQL
2. Create a database named `ecomsme`
3. Update the database settings in `.env`
4. Run migrations: `python manage.py migrate`

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
- **Port 8000 in use**: Change port in `manage.py runserver 8001`
- **Database errors**: Run `python manage.py migrate`
- **Missing dependencies**: Run `pip install -r requirements.txt`

#### Frontend Issues
- **Port 3000 in use**: React will automatically suggest an alternative port
- **API connection errors**: Check if backend is running on port 8000
- **Build errors**: Clear node_modules and reinstall: `rm -rf node_modules && npm install`

#### Docker Issues
- **Port conflicts**: Stop other services using ports 3000, 8000, 5432, 6379
- **Permission errors**: Run with sudo (Linux/macOS) or as administrator (Windows)
- **Build failures**: Clear Docker cache: `docker system prune -a`

### Getting Help

1. Check the logs: `docker-compose logs`
2. Verify all services are running: `docker-compose ps`
3. Restart services: `docker-compose restart`
4. Check the documentation in the `/docs` folder

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [API Documentation](http://localhost:8000/api/docs)
- Check out the [Contributing Guide](CONTRIBUTING.md)
- Join our community discussions

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: support@ecomsme.ai

---

🎉 **Congratulations!** You're now ready to start tracking and reducing your environmental impact with EcoMSME AI! 