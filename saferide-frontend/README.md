# SafeRide - Comprehensive Ride-Sharing Platform

SafeRide is a modern ride-sharing platform with advanced admin portal, role-based access control, company management, and intelligent route planning capabilities.

## 🚀 Features

### Core Platform
- **Modern React + TypeScript Frontend** with Vite
- **FastAPI Python Backend** with comprehensive REST API
- **Role-Based Access Control (RBAC)** with granular permissions
- **JWT Authentication** with secure token management
- **Real-time Dashboard** with analytics and metrics

### Admin Portal Features
- **User Management** - Create, edit, and manage users with role assignments
- **Company Management** - Manage driver companies and their service areas
- **Service Area Management** - Define and manage geographic service areas
- **User Location Management** - Track and manage user locations for route planning
- **Route Planning & Optimization** - Intelligent route optimization for drivers
- **Audit Logging** - Comprehensive activity tracking and logging
- **Analytics Dashboard** - Real-time metrics and performance insights

### Role-Based Access Control
The system implements a comprehensive RBAC system with the following roles:

#### Roles
- **Administrator** - Full system access
- **Manager** - Management level access
- **Support** - Customer support access
- **Driver** - Driver-specific access
- **Rider** - Rider access
- **Company Admin** - Company-level administrator
- **Company Manager** - Company management access

#### Permissions
- User Management (view, create, edit, delete, block)
- Ride Management (view, create, edit, cancel, assign drivers)
- Driver Management (view, approve, suspend, rate)
- Company Management (manage companies, view drivers, assign drivers)
- Service Area Management
- Route Planning (plan routes, view optimization, manage locations)
- Analytics & Reports (view analytics, export reports, view revenue)
- System Settings (manage settings, view logs, manage roles)
- Real-time Monitoring (view live rides, track drivers)

## 🏗️ Architecture

### Frontend (React + TypeScript)
```
src/
├── components/
│   ├── Login.tsx          # Authentication component
│   ├── AdminPortal.tsx    # Comprehensive admin portal
│   └── AdminPortal.css    # Admin portal styles
├── services/
│   ├── apiService.ts      # API communication service
│   └── userService.ts     # User management service
└── data/
    └── users.json         # Mock user data
```

### Backend (FastAPI + Python)
```
saferide-backend-python/
├── main.py               # Main FastAPI application
├── models.py             # Pydantic models and data structures
├── auth.py               # Authentication and authorization
├── requirements.txt      # Python dependencies
└── env.example          # Environment variables template
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.9+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/galak06/SafeRide.git
   cd SafeRide
   ```

2. **Start the Backend**
   ```bash
   cd saferide-backend-python
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```
   The backend will start on `http://localhost:8000`

3. **Start the Frontend**
   ```bash
   npm install
   npm run dev
   ```
   The frontend will start on `http://localhost:3000`

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Default Login Credentials
- **Email**: admin@saferide.com
- **Password**: admin123

## 📊 Admin Portal Features

### Dashboard
- Real-time metrics and KPIs
- User statistics and growth trends
- Revenue analytics
- System health monitoring

### User Management
- Create, edit, and delete users
- Role assignment and management
- User status management (active/inactive)
- Search and filter capabilities
- Pagination support

### Company Management
- Create and manage driver companies
- Assign service areas to companies
- Manage company drivers
- Company status management

### Service Area Management
- Define geographic service areas using coordinates
- Polygon-based area definition
- Area status management
- Visual area representation

### User Location Management
- Track user locations with addresses and coordinates
- Location status management
- Search and filter capabilities
- Bulk location operations

### Route Planning & Optimization
- **Intelligent Route Optimization**
  - Nearest neighbor algorithm
  - Multiple optimization types (shortest distance, fastest route, balanced)
  - Time window constraints
  - Maximum stops configuration

- **Route Management**
  - Create optimized routes for drivers
  - View route details and statistics
  - Route status management
  - Alternative route suggestions

### Audit Logging
- Comprehensive activity tracking
- User action logging
- Resource access monitoring
- IP address and user agent tracking
- Searchable audit logs

## 🔐 Security Features

### Authentication
- JWT token-based authentication
- Secure password hashing with bcrypt
- Token expiration management
- Session management

### Authorization
- Role-based access control (RBAC)
- Granular permission system
- Resource-level access control
- Permission inheritance

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF protection

## 🗺️ Route Planning Algorithm

The system implements an intelligent route optimization algorithm:

### Features
- **Nearest Neighbor Algorithm** for initial route optimization
- **Distance Calculation** using Haversine formula
- **Time Estimation** based on distance and traffic
- **Multiple Optimization Types**:
  - Shortest Distance
  - Fastest Route
  - Balanced (distance + time)

### Process
1. **Location Collection** - Gather user locations for route planning
2. **Optimization** - Apply selected optimization algorithm
3. **Route Generation** - Create optimized route with stops
4. **Statistics Calculation** - Calculate distance, duration, and metrics
5. **Route Storage** - Save optimized route for driver use

## 📈 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Admin Dashboard
- `GET /api/admin/dashboard/metrics` - Get dashboard metrics
- `GET /api/admin/dashboard/user-stats` - Get user statistics

### User Management
- `GET /api/admin/users` - Get paginated users
- `POST /api/admin/users` - Create new user
- `PUT /api/admin/users/{user_id}` - Update user

### Company Management
- `GET /api/admin/companies` - Get paginated companies
- `POST /api/admin/companies` - Create new company
- `GET /api/admin/companies/{company_id}` - Get company details
- `PUT /api/admin/companies/{company_id}` - Update company

### Service Areas
- `GET /api/admin/service-areas` - Get all service areas
- `POST /api/admin/service-areas` - Create new service area

### User Locations
- `GET /api/admin/user-locations` - Get paginated user locations
- `POST /api/admin/user-locations` - Create new user location

### Route Planning
- `POST /api/admin/route-optimization` - Optimize route
- `GET /api/admin/route-plans` - Get paginated route plans

### System Management
- `GET /api/admin/roles` - Get all roles
- `GET /api/admin/permissions` - Get all permissions
- `GET /api/admin/audit-logs` - Get paginated audit logs

## 🛠️ Development

### Frontend Development
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn main:app --reload

# Run tests
pytest
```

### Environment Variables
Create a `.env` file in the backend directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
WAZE_API_KEY=your-waze-api-key
```

## 🧪 Testing

### Frontend Tests
```bash
npm test
npm run test:coverage
```

### Backend Tests
```bash
pytest
pytest --cov=app
```

## 📦 Deployment

### Frontend Deployment
```bash
npm run build
# Deploy dist/ folder to your hosting service
```

### Backend Deployment
```bash
# Using Docker
docker build -t saferide-backend .
docker run -p 8000:8000 saferide-backend

# Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the API documentation at `/docs`

## 📋 TODO

### API Integration Interfaces

- [ ] **Google Maps API Integration**
  - [ ] Create React components for Google Maps integration
  - [ ] Implement map display with route visualization
  - [ ] Add geocoding and reverse geocoding functionality
  - [ ] Implement place search and autocomplete
  - [ ] Add real-time traffic data display
  - [ ] Create route optimization visualization
  - [ ] Add distance and time calculations
  - [ ] Implement map markers and info windows
  - [ ] Add responsive map controls

- [ ] **Waze API Integration**
  - [ ] Create service for Waze API communication
  - [ ] Implement real-time traffic data retrieval
  - [ ] Add traffic incident display on map
  - [ ] Create route optimization with traffic considerations
  - [ ] Implement traffic pattern analysis visualization
  - [ ] Add traffic alerts and notifications
  - [ ] Create traffic heatmap display

- [ ] **Map Service Abstraction**
  - [ ] Create unified map service interface
  - [ ] Implement service provider selection (Google Maps vs Waze)
  - [ ] Add configuration for API keys and endpoints
  - [ ] Create fallback mechanisms between services
  - [ ] Add performance monitoring and error handling
  - [ ] Implement caching for map data

- [ ] **Route Planning UI Enhancements**
  - [ ] Interactive map for route planning
  - [ ] Drag-and-drop route optimization
  - [ ] Real-time route preview
  - [ ] Multiple route comparison
  - [ ] Route sharing and export functionality

## 🔮 Future Enhancements

- **Real-time GPS Tracking** - Live driver and ride tracking
- **Advanced Route Optimization** - Machine learning-based optimization
- **Mobile Applications** - iOS and Android apps
- **Payment Integration** - Stripe, PayPal integration
- **Push Notifications** - Real-time notifications
- **Analytics Dashboard** - Advanced reporting and analytics
- **Multi-language Support** - Internationalization
- **Dark Mode** - Theme customization
- **Offline Support** - Progressive Web App features

---

**SafeRide** - Your trusted ride-sharing platform with advanced admin capabilities and intelligent route planning. 