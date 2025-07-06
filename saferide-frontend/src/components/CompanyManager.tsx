import React, { useState, useEffect } from 'react';
import { companyService, Company, CompanyCreate, Driver } from '../services/companyService';
import MapSelector from './MapSelector';
import './CompanyManager.css';

const CompanyManager: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [availableDrivers, setAvailableDrivers] = useState<Driver[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);

  // Form state
  const [formData, setFormData] = useState<CompanyCreate>({
    name: '',
    description: '',
    contact_email: '',
    contact_phone: '',
    address: '',
    operation_area_type: 'circle',
    center_lat: 40.7128,
    center_lng: -74.0060,
    radius_km: 10,
    is_active: true
  });

  useEffect(() => {
    initializeComponent();
  }, []);

  const initializeComponent = async () => {
    try {
      setIsInitialized(false);
      setError(null);
      await loadCompanies();
      await loadAvailableDrivers();
      setIsInitialized(true);
    } catch (err) {
      console.error('Failed to initialize CompanyManager:', err);
      setError('Failed to initialize company management. Please check your connection and try again.');
      setIsInitialized(true);
    }
  };

  const loadCompanies = async () => {
    try {
      setLoading(true);
      console.log('Loading companies...');
      const data = await companyService.getCompanies();
      console.log('Companies loaded:', data);
      setCompanies(data || []);
    } catch (err: any) {
      console.error('Error loading companies:', err);
      const errorMessage = err.message || 'Failed to load companies';
      setError(errorMessage);
      setCompanies([]);
    } finally {
      setLoading(false);
    }
  };

  const loadAvailableDrivers = async () => {
    try {
      console.log('Loading available drivers...');
      const data = await companyService.getAvailableDrivers();
      console.log('Available drivers loaded:', data);
      setAvailableDrivers(data || []);
    } catch (err: any) {
      console.error('Error loading available drivers:', err);
      // Don't set error for drivers as it's not critical
      setAvailableDrivers([]);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAreaChange = (area: {
    type: 'circle' | 'polygon';
    centerLat?: number;
    centerLng?: number;
    radiusKm?: number;
    polygonCoordinates?: Array<{ lat: number; lng: number }>;
  }) => {
    setFormData(prev => ({
      ...prev,
      operation_area_type: area.type,
      center_lat: area.centerLat,
      center_lng: area.centerLng,
      radius_km: area.radiusKm,
      polygon_coordinates: area.polygonCoordinates
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);
      
      console.log('Creating company with data:', formData);
      await companyService.createCompany(formData);
      
      // Reset form
      setFormData({
        name: '',
        description: '',
        contact_email: '',
        contact_phone: '',
        address: '',
        operation_area_type: 'circle',
        center_lat: 40.7128,
        center_lng: -74.0060,
        radius_km: 10,
        is_active: true
      });
      
      setShowAddForm(false);
      await loadCompanies();
      await loadAvailableDrivers();
    } catch (err: any) {
      console.error('Error creating company:', err);
      const errorMessage = err.message || 'Failed to create company';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleAssignDriver = async (companyId: string, driverId: string) => {
    try {
      console.log('Assigning driver', driverId, 'to company', companyId);
      await companyService.assignDriverToCompany(companyId, driverId);
      await loadCompanies();
      await loadAvailableDrivers();
    } catch (err: any) {
      console.error('Error assigning driver:', err);
      const errorMessage = err.message || 'Failed to assign driver';
      setError(errorMessage);
    }
  };

  const handleRemoveDriver = async (companyId: string, driverId: string) => {
    try {
      console.log('Removing driver', driverId, 'from company', companyId);
      await companyService.removeDriverFromCompany(companyId, driverId);
      await loadCompanies();
      await loadAvailableDrivers();
    } catch (err: any) {
      console.error('Error removing driver:', err);
      const errorMessage = err.message || 'Failed to remove driver';
      setError(errorMessage);
    }
  };

  const handleDeleteCompany = async (companyId: string) => {
    if (!window.confirm('Are you sure you want to delete this company?')) {
      return;
    }

    try {
      console.log('Deleting company:', companyId);
      await companyService.deleteCompany(companyId);
      await loadCompanies();
      await loadAvailableDrivers();
    } catch (err: any) {
      console.error('Error deleting company:', err);
      const errorMessage = err.message || 'Failed to delete company';
      setError(errorMessage);
    }
  };

  const formatAreaInfo = (company: Company) => {
    if (company.operation_area_type === 'circle') {
      return `Circle: ${company.center_lat?.toFixed(4)}, ${company.center_lng?.toFixed(4)} (${company.radius_km}km)`;
    } else {
      return `Polygon: ${company.polygon_coordinates?.length || 0} points`;
    }
  };

  // Show loading state while initializing
  if (!isInitialized) {
    return (
      <div className="company-manager">
        <div className="company-manager-loading">
          <div className="spinner"></div>
          <p>Initializing Company Management...</p>
        </div>
      </div>
    );
  }

  // Show error state if there's a critical error
  if (error && companies.length === 0 && !showAddForm) {
    return (
      <div className="company-manager">
        <div className="company-manager-header">
          <h2>Company Management</h2>
          <button 
            className="btn btn-primary"
            onClick={() => setShowAddForm(true)}
          >
            Add New Company
          </button>
        </div>
        
        <div className="error-message">
          <div>
            <strong>Error:</strong> {error}
          </div>
          <button onClick={initializeComponent} className="btn btn-secondary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="company-manager">
      <div className="company-manager-header">
        <h2>Company Management</h2>
        <button 
          className="btn btn-primary"
          onClick={() => setShowAddForm(!showAddForm)}
        >
          {showAddForm ? 'Cancel' : 'Add New Company'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          <div>{error}</div>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      {showAddForm && (
        <div className="add-company-form">
          <h3>Add New Company</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="name">Company Name *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="contact_email">Contact Email *</label>
                <input
                  type="email"
                  id="contact_email"
                  name="contact_email"
                  value={formData.contact_email}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="contact_phone">Contact Phone</label>
                <input
                  type="tel"
                  id="contact_phone"
                  name="contact_phone"
                  value={formData.contact_phone}
                  onChange={handleInputChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="address">Address</label>
                <input
                  type="text"
                  id="address"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows={3}
              />
            </div>

            <div className="form-group">
              <label>Operation Area</label>
              <MapSelector
                operationAreaType={formData.operation_area_type}
                centerLat={formData.center_lat}
                centerLng={formData.center_lng}
                radiusKm={formData.radius_km}
                polygonCoordinates={formData.polygon_coordinates}
                onAreaChange={handleAreaChange}
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Creating...' : 'Create Company'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => setShowAddForm(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="companies-list">
        <h3>Companies ({companies.length})</h3>
        {loading && companies.length === 0 ? (
          <div className="company-manager-loading">Loading companies...</div>
        ) : companies.length === 0 ? (
          <p className="no-companies">No companies found. Add your first company above.</p>
        ) : (
          <div className="companies-grid">
            {companies.map(company => (
              <div key={company.id} className="company-card">
                <div className="company-header">
                  <h4>{company.name}</h4>
                  <div className="company-status">
                    <span className={`status-badge ${company.is_active ? 'active' : 'inactive'}`}>
                      {company.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>

                <div className="company-details">
                  <p><strong>Email:</strong> {company.contact_email}</p>
                  {company.contact_phone && (
                    <p><strong>Phone:</strong> {company.contact_phone}</p>
                  )}
                  {company.address && (
                    <p><strong>Address:</strong> {company.address}</p>
                  )}
                  <p><strong>Operation Area:</strong> {formatAreaInfo(company)}</p>
                  <p><strong>Drivers:</strong> {company.driver_count}</p>
                </div>

                <div className="company-drivers">
                  <h5>Assigned Drivers</h5>
                  {company.drivers && company.drivers.length > 0 ? (
                    <ul className="drivers-list">
                      {company.drivers.map(driver => (
                        <li key={driver.id} className="driver-item">
                          <span>{driver.first_name} {driver.last_name}</span>
                          <button
                            className="btn btn-small btn-danger"
                            onClick={() => handleRemoveDriver(company.id, driver.id)}
                          >
                            Remove
                          </button>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="no-drivers">No drivers assigned</p>
                  )}

                  {availableDrivers.length > 0 && (
                    <div className="assign-driver">
                      <select
                        onChange={(e) => {
                          if (e.target.value) {
                            handleAssignDriver(company.id, e.target.value);
                            e.target.value = '';
                          }
                        }}
                        defaultValue=""
                      >
                        <option value="">Assign a driver...</option>
                        {availableDrivers.map(driver => (
                          <option key={driver.id} value={driver.id}>
                            {driver.first_name} {driver.last_name}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>

                <div className="company-actions">
                  <button
                    className="btn btn-small btn-danger"
                    onClick={() => handleDeleteCompany(company.id)}
                  >
                    Delete Company
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CompanyManager; 