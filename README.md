# EcoMSME AI - Environmental Impact Tracking Platform

A full-stack web application to help Micro, Small, and Medium Enterprises (MSMEs) track, analyze, and reduce their environmental impact using AI, NLP, and "What-if" simulations.

## 🚀 Features

- **Dashboard-based Analytics**: Track carbon footprint over time with detailed breakdowns
- **AI-Powered Invoice Analysis**: Extract environmental data from invoices using NLP
- **Smart Recommendations**: Get actionable sustainability suggestions
- **What-if Simulator**: Interactive tool to simulate environmental impact of changes
- **Multi-language Support**: Internationalization for global MSMEs
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Tech Stack

### Frontend
- React 18 with TypeScript
- Tailwind CSS for styling
- Chart.js for data visualization
- React Router for navigation
- i18next for internationalization
- Axios for API communication

### Backend
- Django 4.2 with Django REST Framework
- PostgreSQL database
- JWT authentication
- Celery + Redis for async tasks
- AWS S3 for file storage

### AI/NLP Engine
- spaCy for entity extraction
- Transformers (BERT) for advanced NLP
- Pandas & NumPy for data processing
- Scikit-learn for ML models

## 📁 Project Structure

```
EcoMSME/
├── backend/
│   ├── eco_api/              # Django REST API
│   ├── nlp_module/           # AI/NLP processing
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── pages/           # Main page components
│   │   ├── components/      # Reusable components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── tailwind.config.js
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL
- Redis

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Docker Setup
```bash
docker-compose up -d
```

## 🔧 Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/ecomsme

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your-jwt-secret
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Invoices
- `POST /api/invoices/upload/` - Upload invoice
- `GET /api/invoices/` - List user invoices
- `GET /api/invoices/{id}/` - Get invoice details

### Analytics
- `GET /api/analytics/carbon-score/` - Get carbon score
- `GET /api/analytics/breakdown/` - Get environmental breakdown
- `GET /api/analytics/timeline/` - Get historical data

### AI Recommendations
- `GET /api/recommendations/` - Get AI suggestions
- `POST /api/simulations/what-if/` - Run what-if simulation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@ecomsme.ai or create an issue in the repository. 