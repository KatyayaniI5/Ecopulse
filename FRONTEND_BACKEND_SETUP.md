# Frontend-Backend Connection Setup Guide

## 🚀 Overview

Your EPICS Project now has a fully configured frontend-backend connection with:
- **Backend**: Django REST API running on `http://localhost:8000`
- **Frontend**: React application running on `http://localhost:3000`
- **API Communication**: Configured with Axios and proper CORS settings

## ✅ Configuration Status

### Backend Configuration ✅
- **CORS Headers**: Properly configured for frontend communication
- **JWT Authentication**: Set up with access and refresh tokens
- **API Endpoints**: All modules available (`/api/auth/`, `/api/invoices/`, etc.)
- **Database**: SQLite with all migrations applied
- **Admin Interface**: Accessible at `http://localhost:8000/admin/`

### Frontend Configuration ✅
- **Axios Setup**: Configured with interceptors for token management
- **Proxy Configuration**: Set to `http://localhost:8000` in package.json
- **API Services**: All endpoints mapped in `src/services/api.js`
- **State Management**: Zustand for global state
- **Routing**: React Router for navigation

## 🔧 How to Start Both Services

### 1. Start Backend (Django)
```bash
cd backend
python manage.py runserver
```
Backend will be available at: `http://localhost:8000`

### 2. Start Frontend (React)
```bash
cd frontend
npm start
```
Frontend will be available at: `http://localhost:3000`

## 🧪 Testing the Connection

### 1. API Test Page
Visit: `http://localhost:3000/api-test`
This page will automatically test the connection and show:
- ✅ Backend connection status
- ✅ Available API endpoints
- ✅ Real-time connection testing

### 2. Manual Testing
You can test individual endpoints:

**Backend Root:**
```bash
curl http://localhost:8000/
```

**Auth API:**
```bash
curl http://localhost:8000/api/auth/
```

**Admin Interface:**
Visit: `http://localhost:8000/admin/`
Login with: `lokesh_04` and your password

## 📡 API Endpoints Available

### Authentication (`/api/auth/`)
- `POST /api/auth/token/` - Login and get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/register/` - User registration
- `GET /api/auth/profile/` - Get user profile

### Invoices (`/api/invoices/`)
- `POST /api/invoices/upload/` - Upload invoice
- `GET /api/invoices/` - List all invoices
- `GET /api/invoices/{id}/` - Get specific invoice
- `DELETE /api/invoices/{id}/delete/` - Delete invoice

### Analytics (`/api/analytics/`)
- `GET /api/analytics/carbon-score/` - Get carbon footprint data
- `GET /api/analytics/breakdown/` - Get environmental breakdown
- `GET /api/analytics/timeline/` - Get timeline data

### Recommendations (`/api/recommendations/`)
- `GET /api/recommendations/` - Get all recommendations
- `GET /api/recommendations/{category}/` - Get by category
- `POST /api/recommendations/{id}/implement/` - Mark as implemented

### Simulations (`/api/simulations/`)
- `POST /api/simulations/what-if/` - Run what-if scenarios
- `GET /api/simulations/scenarios/` - Get available scenarios
- `POST /api/simulations/save/` - Save scenario

## 🔐 Authentication Flow

1. **Login**: User submits credentials to `/api/auth/token/`
2. **Token Storage**: Frontend stores access and refresh tokens
3. **API Calls**: Axios automatically adds `Authorization: Bearer <token>` header
4. **Token Refresh**: When access token expires, refresh token is used automatically
5. **Logout**: Tokens are cleared from localStorage

## 🛠️ Development Workflow

### Making API Calls from Frontend
```javascript
import { authAPI, invoiceAPI } from '../services/api';

// Login
const login = async (credentials) => {
  try {
    const response = await authAPI.login(credentials);
    // Tokens are automatically stored
    return response;
  } catch (error) {
    console.error('Login failed:', error);
  }
};

// Upload invoice
const uploadInvoice = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await invoiceAPI.upload(formData);
    return response;
  } catch (error) {
    console.error('Upload failed:', error);
  }
};
```

### Error Handling
The API service includes automatic error handling:
- **401 Unauthorized**: Automatically attempts token refresh
- **Network Errors**: Shows user-friendly error messages
- **Validation Errors**: Displays field-specific error messages

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend is running on port 8000
   - Check CORS settings in `backend/eco_api/settings.py`

2. **Connection Refused**
   - Verify both services are running
   - Check firewall settings
   - Ensure ports 3000 and 8000 are available

3. **Authentication Issues**
   - Clear localStorage and re-login
   - Check JWT token expiration settings
   - Verify user exists in database

4. **API Endpoint Not Found**
   - Check URL patterns in `backend/eco_api/urls.py`
   - Ensure app is included in `INSTALLED_APPS`

### Debug Commands
```bash
# Check backend status
curl http://localhost:8000/

# Check frontend proxy
curl http://localhost:3000/api/auth/

# Check database migrations
python manage.py showmigrations

# Check running processes
netstat -an | findstr :3000
netstat -an | findstr :8000
```

## 🎯 Next Steps

1. **Test the API Test Page**: Visit `http://localhost:3000/api-test`
2. **Explore the Admin Interface**: Visit `http://localhost:8000/admin/`
3. **Test Authentication**: Try logging in through the frontend
4. **Upload Test Data**: Use the invoice upload functionality
5. **Explore Analytics**: Check the carbon footprint calculations

## 📞 Support

If you encounter any issues:
1. Check the browser console for frontend errors
2. Check the Django logs in `backend/logs/django.log`
3. Verify both services are running on the correct ports
4. Test individual endpoints using curl or Postman

Your frontend-backend connection is now fully configured and ready for development! 🚀