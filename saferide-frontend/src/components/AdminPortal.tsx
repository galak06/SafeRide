import React, { useState, useEffect } from 'react';
import './AdminPortal.css';
import RelationshipManager from './RelationshipManager';

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: {
    id: string;
    name: string;
    description: string;
  };
  is_active: boolean;
  created_at: string;
}

interface Company {
  id: string;
  name: string;
  description: string;
  address: string;
  phone: string;
  email: string;
  service_areas: string[];
  drivers: string[];
  is_active: boolean;
}

interface ServiceArea {
  id: string;
  name: string;
  description: string;
  coordinates: Array<{ lat: number; lng: number }>;
  is_active: boolean;
}

interface UserLocation {
  id: string;
  user_id: string;
  address: string;
  latitude: number;
  longitude: number;
  is_active: boolean;
}

interface RoutePlan {
  id: string;
  company_id: string;
  driver_id: string;
  name: string;
  description: string;
  stops: Array<{
    location_id: string;
    user_id: string;
    address: string;
    latitude: number;
    longitude: number;
    order: number;
  }>;
  total_distance: number;
  estimated_duration: number;
  is_active: boolean;
}

interface DashboardMetrics {
  total_users: number;
  total_rides: number;
  total_revenue: number;
  active_drivers: number;
  pending_rides: number;
  completed_rides_today: number;
  revenue_today: number;
  total_companies: number;
  active_service_areas: number;
}

// Add prop type for onLogout
interface AdminPortalProps {
  onLogout: () => Promise<void>;
}

const AdminPortal: React.FC<AdminPortalProps> = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [users, setUsers] = useState<User[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [serviceAreas, setServiceAreas] = useState<ServiceArea[]>([]);
  const [userLocations, setUserLocations] = useState<UserLocation[]>([]);
  const [routePlans, setRoutePlans] = useState<RoutePlan[]>([]);
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [currentUser, setCurrentUser] = useState<any>(null);

  // Mock data for demonstration
  useEffect(() => {
    // Simulate loading user data
    setCurrentUser({
      id: 'admin-001',
      email: 'admin@saferide.com',
      first_name: 'Admin',
      last_name: 'User',
      role: { id: 'admin', name: 'Administrator', description: 'Full system access' }
    });

    // Mock dashboard metrics
    setMetrics({
      total_users: 1250,
      total_rides: 3450,
      total_revenue: 15000.0,
      active_drivers: 25,
      pending_rides: 5,
      completed_rides_today: 45,
      revenue_today: 1200.0,
      total_companies: 8,
      active_service_areas: 12
    });

    // Mock users
    setUsers([
      {
        id: 'user-1',
        email: 'john.doe@example.com',
        first_name: 'John',
        last_name: 'Doe',
        role: { id: 'driver', name: 'Driver', description: 'Driver access' },
        is_active: true,
        created_at: '2024-01-15T10:30:00Z'
      },
      {
        id: 'user-2',
        email: 'jane.smith@example.com',
        first_name: 'Jane',
        last_name: 'Smith',
        role: { id: 'rider', name: 'Rider', description: 'Rider access' },
        is_active: true,
        created_at: '2024-01-16T14:20:00Z'
      }
    ]);

    // Mock companies
    setCompanies([
      {
        id: 'company-1',
        name: 'City Transport Co.',
        description: 'Premium city transportation services',
        address: '123 Main St, Downtown',
        phone: '+1-555-0123',
        email: 'info@citytransport.com',
        service_areas: ['area-1', 'area-2'],
        drivers: ['driver-1', 'driver-2'],
        is_active: true
      },
      {
        id: 'company-2',
        name: 'Metro Rides',
        description: 'Metropolitan area ride services',
        address: '456 Oak Ave, Midtown',
        phone: '+1-555-0456',
        email: 'contact@metrorides.com',
        service_areas: ['area-3'],
        drivers: ['driver-3'],
        is_active: true
      }
    ]);

    // Mock service areas
    setServiceAreas([
      {
        id: 'area-1',
        name: 'Downtown District',
        description: 'Central business district',
        coordinates: [
          { lat: 40.7128, lng: -74.0060 },
          { lat: 40.7589, lng: -73.9851 },
          { lat: 40.7505, lng: -73.9934 }
        ],
        is_active: true
      },
      {
        id: 'area-2',
        name: 'Midtown Manhattan',
        description: 'Midtown business and entertainment area',
        coordinates: [
          { lat: 40.7589, lng: -73.9851 },
          { lat: 40.7505, lng: -73.9934 },
          { lat: 40.7484, lng: -73.9857 }
        ],
        is_active: true
      }
    ]);

    // Mock user locations
    setUserLocations([
      {
        id: 'location-1',
        user_id: 'user-1',
        address: '123 Broadway, New York, NY',
        latitude: 40.7128,
        longitude: -74.0060,
        is_active: true
      },
      {
        id: 'location-2',
        user_id: 'user-2',
        address: '456 5th Ave, New York, NY',
        latitude: 40.7589,
        longitude: -73.9851,
        is_active: true
      }
    ]);

    // Mock route plans
    setRoutePlans([
      {
        id: 'route-1',
        company_id: 'company-1',
        driver_id: 'driver-1',
        name: 'Morning Pickup Route',
        description: 'Optimized morning pickup route for downtown area',
        stops: [
          {
            location_id: 'location-1',
            user_id: 'user-1',
            address: '123 Broadway, New York, NY',
            latitude: 40.7128,
            longitude: -74.0060,
            order: 1
          },
          {
            location_id: 'location-2',
            user_id: 'user-2',
            address: '456 5th Ave, New York, NY',
            latitude: 40.7589,
            longitude: -73.9851,
            order: 2
          }
        ],
        total_distance: 2.5,
        estimated_duration: 15,
        is_active: true
      }
    ]);
  }, []);

  const renderDashboard = () => (
    <div className="dashboard">
      <h2>Dashboard Overview</h2>
      {metrics && (
        <div className="metrics-grid">
          <div className="metric-card">
            <h3>Total Users</h3>
            <p className="metric-value">{metrics.total_users}</p>
          </div>
          <div className="metric-card">
            <h3>Total Rides</h3>
            <p className="metric-value">{metrics.total_rides}</p>
          </div>
          <div className="metric-card">
            <h3>Active Drivers</h3>
            <p className="metric-value">{metrics.active_drivers}</p>
          </div>
          <div className="metric-card">
            <h3>Pending Rides</h3>
            <p className="metric-value">{metrics.pending_rides}</p>
          </div>
          <div className="metric-card">
            <h3>Companies</h3>
            <p className="metric-value">{metrics.total_companies}</p>
          </div>
          <div className="metric-card">
            <h3>Service Areas</h3>
            <p className="metric-value">{metrics.active_service_areas}</p>
          </div>
        </div>
      )}
    </div>
  );

  const renderUsers = () => (
    <div className="users-section">
      <div className="section-header">
        <h2>User Management</h2>
        <button className="btn-primary">Add New User</button>
      </div>
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}>
                <td>{user.first_name} {user.last_name}</td>
                <td>{user.email}</td>
                <td>
                  <span className={`role-badge role-${user.role.id}`}>
                    {user.role.name}
                  </span>
                </td>
                <td>
                  <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                <td>
                  <button className="btn-small">Edit</button>
                  <button className="btn-small btn-danger">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderCompanies = () => (
    <div className="companies-section">
      <div className="section-header">
        <h2>Company Management</h2>
        <button className="btn-primary">Add New Company</button>
      </div>
      <div className="companies-grid">
        {companies.map(company => (
          <div key={company.id} className="company-card">
            <div className="company-header">
              <h3>{company.name}</h3>
              <span className={`status-badge ${company.is_active ? 'active' : 'inactive'}`}>
                {company.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <p className="company-description">{company.description}</p>
            <div className="company-details">
              <p><strong>Address:</strong> {company.address}</p>
              <p><strong>Phone:</strong> {company.phone}</p>
              <p><strong>Email:</strong> {company.email}</p>
              <p><strong>Drivers:</strong> {company.drivers.length}</p>
              <p><strong>Service Areas:</strong> {company.service_areas.length}</p>
            </div>
            <div className="company-actions">
              <button className="btn-small">Edit</button>
              <button className="btn-small">View Drivers</button>
              <button className="btn-small">Manage Areas</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderServiceAreas = () => (
    <div className="service-areas-section">
      <div className="section-header">
        <h2>Service Areas</h2>
        <button className="btn-primary">Add New Service Area</button>
      </div>
      <div className="areas-grid">
        {serviceAreas.map(area => (
          <div key={area.id} className="area-card">
            <div className="area-header">
              <h3>{area.name}</h3>
              <span className={`status-badge ${area.is_active ? 'active' : 'inactive'}`}>
                {area.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <p className="area-description">{area.description}</p>
            <div className="area-coordinates">
              <p><strong>Coordinates:</strong> {area.coordinates.length} points</p>
            </div>
            <div className="area-actions">
              <button className="btn-small">Edit</button>
              <button className="btn-small">View Map</button>
              <button className="btn-small btn-danger">Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderUserLocations = () => (
    <div className="user-locations-section">
      <div className="section-header">
        <h2>User Locations</h2>
        <button className="btn-primary">Add New Location</button>
      </div>
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Address</th>
              <th>Coordinates</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {userLocations.map(location => (
              <tr key={location.id}>
                <td>{location.user_id}</td>
                <td>{location.address}</td>
                <td>{location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}</td>
                <td>
                  <span className={`status-badge ${location.is_active ? 'active' : 'inactive'}`}>
                    {location.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>
                  <button className="btn-small">Edit</button>
                  <button className="btn-small">View Map</button>
                  <button className="btn-small btn-danger">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderRoutePlanning = () => (
    <div className="route-planning-section">
      <div className="section-header">
        <h2>Route Planning</h2>
        <button className="btn-primary">Create New Route</button>
      </div>
      
      <div className="route-optimization-panel">
        <h3>Route Optimization</h3>
        <div className="optimization-form">
          <div className="form-group">
            <label>Company:</label>
            <select>
              <option>Select Company</option>
              {companies.map(company => (
                <option key={company.id} value={company.id}>{company.name}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Driver:</label>
            <select>
              <option>Select Driver</option>
              <option value="driver-1">John Smith</option>
              <option value="driver-2">Sarah Johnson</option>
            </select>
          </div>
          <div className="form-group">
            <label>User Locations:</label>
            <div className="location-selector">
              {userLocations.map(location => (
                <label key={location.id} className="location-checkbox">
                  <input type="checkbox" />
                  {location.address}
                </label>
              ))}
            </div>
          </div>
          <div className="form-group">
            <label>Optimization Type:</label>
            <select>
              <option value="shortest_distance">Shortest Distance</option>
              <option value="fastest_route">Fastest Route</option>
              <option value="balanced">Balanced</option>
            </select>
          </div>
          <button className="btn-primary">Optimize Route</button>
        </div>
      </div>

      <div className="route-plans-list">
        <h3>Route Plans</h3>
        <div className="route-plans-grid">
          {routePlans.map(plan => (
            <div key={plan.id} className="route-plan-card">
              <div className="route-plan-header">
                <h4>{plan.name}</h4>
                <span className={`status-badge ${plan.is_active ? 'active' : 'inactive'}`}>
                  {plan.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <p className="route-description">{plan.description}</p>
              <div className="route-stats">
                <p><strong>Stops:</strong> {plan.stops.length}</p>
                <p><strong>Distance:</strong> {plan.total_distance} km</p>
                <p><strong>Duration:</strong> {plan.estimated_duration} min</p>
              </div>
              <div className="route-stops">
                <h5>Stops:</h5>
                <ol>
                  {plan.stops.map((stop, index) => (
                    <li key={index}>{stop.address}</li>
                  ))}
                </ol>
              </div>
              <div className="route-actions">
                <button className="btn-small">View Map</button>
                <button className="btn-small">Edit</button>
                <button className="btn-small btn-danger">Delete</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return renderDashboard();
      case 'users':
        return renderUsers();
      case 'companies':
        return renderCompanies();
      case 'service-areas':
        return renderServiceAreas();
      case 'user-locations':
        return renderUserLocations();
      case 'route-planning':
        return renderRoutePlanning();
      case 'relationships':
        return <RelationshipManager userId={currentUser?.id} />;
      default:
        return renderDashboard();
    }
  };

  return (
    <div className="admin-portal">
      <div className="admin-header">
        <h1>SafeRide Admin Portal</h1>
        <div className="user-info">
          <span>Welcome, {currentUser?.first_name} {currentUser?.last_name}</span>
          <span className="user-role">{currentUser?.role?.name}</span>
          <button className="logout-button" onClick={onLogout}>Logout</button>
        </div>
      </div>

      <div className="admin-layout">
        <nav className="admin-sidebar">
          <ul className="nav-menu">
            <li className={activeTab === 'dashboard' ? 'active' : ''}>
              <button onClick={() => setActiveTab('dashboard')}>
                📊 Dashboard
              </button>
            </li>
            <li className={activeTab === 'users' ? 'active' : ''}>
              <button onClick={() => setActiveTab('users')}>
                👥 Users
              </button>
            </li>
            <li className={activeTab === 'companies' ? 'active' : ''}>
              <button onClick={() => setActiveTab('companies')}>
                🏢 Companies
              </button>
            </li>
            <li className={activeTab === 'service-areas' ? 'active' : ''}>
              <button onClick={() => setActiveTab('service-areas')}>
                🗺️ Service Areas
              </button>
            </li>
            <li className={activeTab === 'user-locations' ? 'active' : ''}>
              <button onClick={() => setActiveTab('user-locations')}>
                📍 User Locations
              </button>
            </li>
            <li className={activeTab === 'route-planning' ? 'active' : ''}>
              <button onClick={() => setActiveTab('route-planning')}>
                🚗 Route Planning
              </button>
            </li>
            <li className={activeTab === 'relationships' ? 'active' : ''}>
              <button onClick={() => setActiveTab('relationships')}>
                👨‍👩‍👧‍👦 Relationships
              </button>
            </li>
          </ul>
        </nav>

        <main className="admin-content">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default AdminPortal; 