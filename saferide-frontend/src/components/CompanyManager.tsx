import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { companyService, Company, CompanyCreate, Driver } from '../services/companyService';
import { useLanguage } from '../contexts/LanguageContext';
import MapSelector from './MapSelector';
import './CompanyManager.css';

export interface CompanyManagerRef {
  closeForm: () => void;
}

const CompanyManager = forwardRef<CompanyManagerRef>((props, ref) => {
  const { t } = useLanguage();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [availableDrivers, setAvailableDrivers] = useState<Driver[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const defaultFormData: CompanyCreate = {
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
  };

  // Atomic state for form and visibility
  interface CompanyFormState {
    showAddForm: boolean;
    formData: CompanyCreate;
  }

  const getInitialCompanyFormState = (): CompanyFormState => {
    const savedShowForm = localStorage.getItem('companyShowAddForm');
    const savedFormData = localStorage.getItem('companyFormData');
    if (savedShowForm === 'true') {
      if (savedFormData) {
        try {
          return {
            showAddForm: true,
            formData: JSON.parse(savedFormData)
          };
        } catch (e) {
          console.warn('Failed to parse saved form data:', e);
        }
      }
      return { showAddForm: true, formData: { ...defaultFormData } };
    }
    return { showAddForm: false, formData: { ...defaultFormData } };
  };

  const [companyFormState, setCompanyFormState] = useState<CompanyFormState>(getInitialCompanyFormState);
  const { showAddForm, formData } = companyFormState;
  const [isInitialized, setIsInitialized] = useState(false);
  // Add edit mode state
  const [editCompanyId, setEditCompanyId] = useState<string | null>(null);

  // Expose closeForm method to parent component
  useImperativeHandle(ref, () => ({
    closeForm: () => {
      setCompanyFormState({ showAddForm: false, formData: { ...defaultFormData } });
    }
  }));

  // Save to localStorage whenever state changes
  useEffect(() => {
    localStorage.setItem('companyShowAddForm', JSON.stringify(showAddForm));
    localStorage.setItem('companyFormData', JSON.stringify(formData));
  }, [showAddForm, formData]);

  // Restore showAddForm state from localStorage
  useEffect(() => {
    const savedShowForm = localStorage.getItem('companyShowAddForm');
    if (savedShowForm) {
      setCompanyFormState(prev => ({ ...prev, showAddForm: JSON.parse(savedShowForm) }));
    }
  }, []);

  // When clicking Add New Company, clear form and localStorage
  const handleShowAddForm = () => {
    if (!showAddForm) {
      setCompanyFormState({ showAddForm: true, formData: { ...defaultFormData } });
    } else {
      setCompanyFormState({ showAddForm: false, formData: { ...defaultFormData } });
    }
  };

  // When clicking Edit, populate form and switch to edit mode
  const handleEditCompany = (company: Company) => {
    setCompanyFormState({ showAddForm: true, formData: { ...company } });
    setEditCompanyId(company.id);
    // Scroll to top to show the form
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Cancel edit
  const handleCancelEdit = () => {
    setCompanyFormState({ showAddForm: false, formData: { ...defaultFormData } });
    setEditCompanyId(null);
  };

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
      setError(t('companies.errors.loadFailed'));
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
      const errorMessage = err.message || t('companies.errors.loadFailed');
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

  // Update form data
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setCompanyFormState(prev => ({
      ...prev,
      formData: {
        ...prev.formData,
        [name]: value
      }
    }));
  };

  const handleAreaChange = (area: {
    type: 'circle' | 'polygon';
    centerLat?: number;
    centerLng?: number;
    radiusKm?: number;
    polygonCoordinates?: Array<{ lat: number; lng: number }>;
  }) => {
    setCompanyFormState(prev => ({
      ...prev,
      formData: {
        ...prev.formData,
        operation_area_type: area.type,
        center_lat: area.centerLat,
        center_lng: area.centerLng,
        radius_km: area.radiusKm,
        polygon_coordinates: area.polygonCoordinates
      }
    }));
  };

  // Update form submission logic
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      if (editCompanyId) {
        await companyService.updateCompany(editCompanyId, formData);
      } else {
        await companyService.createCompany(formData);
      }
      setCompanyFormState({ showAddForm: false, formData: { ...defaultFormData } });
      setEditCompanyId(null);
      await loadCompanies();
      await loadAvailableDrivers();
    } catch (err: any) {
      console.error('Error saving company:', err);
      const errorMessage = err.message || t('companies.errors.createFailed');
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
      const errorMessage = err.message || t('companies.errors.assignFailed');
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
      const errorMessage = err.message || t('companies.errors.removeFailed');
      setError(errorMessage);
    }
  };

  const handleDeleteCompany = async (companyId: string) => {
    if (!window.confirm(t('companies.deleteConfirm'))) {
      return;
    }

    try {
      console.log('Deleting company:', companyId);
      await companyService.deleteCompany(companyId);
      await loadCompanies();
      await loadAvailableDrivers();
    } catch (err: any) {
      console.error('Error deleting company:', err);
      const errorMessage = err.message || t('companies.errors.deleteFailed');
      setError(errorMessage);
    }
  };

  const formatAreaInfo = (company: Company) => {
    if (company.operation_area_type === 'circle') {
      return `${t('companies.circle')}: ${company.center_lat?.toFixed(4)}, ${company.center_lng?.toFixed(4)} (${company.radius_km}km)`;
    } else {
      return `${t('companies.polygon')}: ${company.polygon_coordinates?.length || 0} ${t('common.points')}`;
    }
  };

  // Show loading state while initializing
  if (!isInitialized) {
    return (
      <div className="company-manager">
        <div className="company-manager-loading">
          <div className="spinner"></div>
          <p>{t('companies.loadingCompanies')}</p>
        </div>
      </div>
    );
  }

  // Show error state if there's a critical error
  if (error && companies.length === 0 && !showAddForm) {
    return (
      <div className="company-manager">
        <div className="company-manager-header">
          <h2>{t('companies.title')}</h2>
          <button 
            className="btn btn-primary"
            onClick={() => setCompanyFormState(prev => ({ ...prev, showAddForm: true }))}
          >
            {t('companies.addCompany')}
          </button>
        </div>
        
        <div className="error-message">
          <div>
            <strong>{t('common.error')}:</strong> {error}
          </div>
          <button onClick={initializeComponent} className="btn btn-secondary">
            {t('common.retry')}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="company-manager">
      <div className="company-manager-header">
        <h2>{t('companies.title')}</h2>
        <button 
          className="btn btn-primary"
          onClick={handleShowAddForm}
        >
          {showAddForm ? t('common.cancel') : t('companies.addCompany')}
        </button>
      </div>

      {error && (
        <div className="error-message">
          <div>{error}</div>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      {showAddForm && (
        <form onSubmit={handleSubmit} className="company-form">
          <h3>{editCompanyId ? (formData.name || 'Edit Company') : (t('companies.addTitle') || 'Add Company')}</h3>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="name">{t('companies.companyName')} *</label>
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
                <label htmlFor="contact_email">{t('companies.contactEmail')} *</label>
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
                <label htmlFor="contact_phone">{t('companies.contactPhone')}</label>
                <input
                  type="tel"
                  id="contact_phone"
                  name="contact_phone"
                  value={formData.contact_phone}
                  onChange={handleInputChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="address">{t('companies.address')}</label>
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
              <label htmlFor="description">{t('companies.description')}</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows={3}
              />
            </div>

            <div className="form-group">
              <label>{t('companies.operationArea')}</label>
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
                {loading ? t('companies.creating') : (editCompanyId ? 'Save' : t('companies.createCompany'))}
              </button>
              {editCompanyId && <button type="button" onClick={handleCancelEdit} className="btn btn-secondary">{t('companies.cancelEdit')}</button>}
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => setCompanyFormState(prev => ({ ...prev, showAddForm: false }))}
              >
                {t('common.cancel')}
              </button>
            </div>
          </form>
      )}

      <div className="companies-list">
        <h3>{t('companies.title')} ({companies.length})</h3>
        {loading && companies.length === 0 ? (
          <div className="company-manager-loading">{t('companies.loadingCompanies')}</div>
        ) : companies.length === 0 ? (
          <p className="no-companies">{t('companies.noCompanies')}</p>
        ) :
          <div className="companies-grid">
            {companies.map(company => (
              <div key={company.id} className="company-card">
                <div className="company-header">
                  <h4>{company.name}</h4>
                  <div className="company-status">
                    <span className={`status-badge ${company.is_active ? 'active' : 'inactive'}`}>
                      {company.is_active ? t('common.active') : t('common.inactive')}
                    </span>
                  </div>
                </div>

                <div className="company-details">
                  <p><strong>{t('auth.email')}:</strong> {company.contact_email}</p>
                  {company.contact_phone && (
                    <p><strong>{t('companies.contactPhone')}:</strong> {company.contact_phone}</p>
                  )}
                  {company.address && (
                    <p><strong>{t('companies.address')}:</strong> {company.address}</p>
                  )}
                  <p><strong>{t('companies.operationArea')}:</strong> {formatAreaInfo(company)}</p>
                  <p><strong>{t('companies.drivers')}:</strong> {company.driver_count}</p>
                </div>

                {company.drivers && company.drivers.length > 0 && (
                  <div className="company-drivers">
                    <h5>{t('companies.assignedDrivers')}</h5>
                    <div className="drivers-list">
                      {company.drivers.map(driver => (
                        <div key={driver.id} className="driver-item">
                          <span>{driver.first_name} {driver.last_name}</span>
                          <button
                            className="btn-small btn-danger"
                            onClick={() => handleRemoveDriver(company.id, driver.id)}
                            title={t('companies.removeDriver')}
                          >
                            {t('companies.removeDriver')}
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="company-actions">
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
                        <option value="">{t('companies.assignDriver')}</option>
                        {availableDrivers.map(driver => (
                          <option key={driver.id} value={driver.id}>
                            {driver.first_name} {driver.last_name}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                  
                  <button
                    className="btn-small btn-danger"
                    onClick={() => handleDeleteCompany(company.id)}
                    title={t('companies.deleteCompany')}
                  >
                    {t('common.delete')}
                  </button>
                  <button
                    className="btn-small btn-primary"
                    onClick={() => handleEditCompany(company)}
                    title={t('companies.editCompany')}
                  >
                    Edit
                  </button>
                </div>
              </div>
            ))}
          </div>
        }
      </div>
    </div>
  );
});

export default CompanyManager; 