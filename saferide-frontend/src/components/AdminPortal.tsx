import React, { useState, useEffect, useRef } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import { dashboardService, DashboardMetrics } from '../services/dashboardService'
import ChildrenManager from './ChildrenManager'
import CompanyManager from './CompanyManager'
import './AdminPortal.css'

interface AdminPortalProps {}

const AdminPortal: React.FC<AdminPortalProps> = () => {
  const { t } = useLanguage()
  const companyManagerRef = useRef<{ closeForm: () => void }>(null);
  const childrenManagerRef = useRef<{ closeForm: () => void }>(null);
  
  // Dashboard metrics state
  const [dashboardMetrics, setDashboardMetrics] = useState<DashboardMetrics>({
    total_users: 0,
    active_users: 0,
    total_drivers: 0,
    active_drivers: 0,
    total_companies: 0,
    active_companies: 0,
    total_children: 0,
    active_rides: 0,
    timestamp: new Date().toISOString(),
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  // Initialize activeTab with localStorage persistence
  const [activeTab, setActiveTab] = useState<'dashboard' | 'companies' | 'children'>(() => {
    // Try to restore active tab from localStorage on component mount
    const savedTab = localStorage.getItem('adminActiveTab');
    if (savedTab && ['dashboard', 'companies', 'children'].includes(savedTab)) {
      return savedTab as 'dashboard' | 'companies' | 'children';
    }
    return 'dashboard';
  });

  // Save active tab to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('adminActiveTab', activeTab);
  }, [activeTab]);

  // Fetch dashboard metrics on component mount and when dashboard tab is active
  useEffect(() => {
    const fetchDashboardMetrics = async () => {
      if (activeTab === 'dashboard') {
        setLoading(true);
        setError(null);
        
        try {
          const metrics = await dashboardService.getFormattedMetrics();
          setDashboardMetrics(metrics);
        } catch (err) {
          console.error('Failed to fetch dashboard metrics:', err);
          setError('Failed to load dashboard data');
        } finally {
          setLoading(false);
        }
      }
    };

    fetchDashboardMetrics();
  }, [activeTab]);

  const handleTabClick = (tab: 'dashboard' | 'companies' | 'children') => {
    // If clicking on companies tab, close any open forms
    if (tab === 'companies' && companyManagerRef.current) {
      companyManagerRef.current.closeForm();
    }
    // If clicking on children tab, close any open forms
    if (tab === 'children' && childrenManagerRef.current) {
      childrenManagerRef.current.closeForm();
    }
    setActiveTab(tab);
  };

  return (
    <div className="admin-portal">
      <div className="admin-header">
        <h1>{t('admin.portal')}</h1>
        <p>{t('admin.manageDrivers')}</p>
      </div>
      
      <div className="admin-tabs">
        <button
          className={`tab-button ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => handleTabClick('dashboard')}
        >
          {t('admin.dashboard')}
        </button>
        <button
          className={`tab-button ${activeTab === 'companies' ? 'active' : ''}`}
          onClick={() => handleTabClick('companies')}
        >
          {t('admin.companies')}
        </button>
        <button
          className={`tab-button ${activeTab === 'children' ? 'active' : ''}`}
          onClick={() => handleTabClick('children')}
        >
          {t('admin.children')}
        </button>
      </div>
      
      <div className="admin-content">
        {activeTab === 'dashboard' && (
          <div className="dashboard">
            <h2>{t('admin.systemDashboard')}</h2>
            
            {loading && (
              <div className="loading">{t('common.loading')}</div>
            )}
            
            {error && (
              <div className="error-message">{error}</div>
            )}
            
            {!loading && !error && (
              <>
                <div className="dashboard-stats">
                  <div className="stat-card">
                    <h3>{t('admin.totalDrivers')}</h3>
                    <div className="stat-number">{dashboardMetrics.total_drivers}</div>
                    <p>{t('admin.activeDrivers')}: {dashboardMetrics.active_drivers}</p>
                  </div>
                  <div className="stat-card">
                    <h3>{t('admin.totalCompanies')}</h3>
                    <div className="stat-number">{dashboardMetrics.total_companies}</div>
                    <p>{t('admin.registeredCompanies')}: {dashboardMetrics.active_companies}</p>
                  </div>
                  <div className="stat-card">
                    <h3>{t('admin.totalChildren')}</h3>
                    <div className="stat-number">{dashboardMetrics.total_children}</div>
                    <p>{t('admin.childrenInSystem')}</p>
                  </div>
                  <div className="stat-card">
                    <h3>{t('admin.activeRides')}</h3>
                    <div className="stat-number">{dashboardMetrics.active_rides}</div>
                    <p>{t('admin.ridesInProgress')}</p>
                  </div>
                </div>
                
                <div className="dashboard-recent">
                  <h3>{t('admin.recentActivity')}</h3>
                  <div className="activity-list">
                    <div className="activity-item">
                      <span className="activity-time">Just now</span>
                      <span className="activity-text">{t('admin.systemInitialized')}</span>
                    </div>
                    <div className="activity-item">
                      <span className="activity-time">2 minutes ago</span>
                      <span className="activity-text">{t('admin.adminPortalAccessed')}</span>
                    </div>
                    <div className="activity-item">
                      <span className="activity-time">Last updated</span>
                      <span className="activity-text">
                        Dashboard metrics updated at {new Date(dashboardMetrics.timestamp).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        )}
        
        {activeTab === 'companies' && (
          <CompanyManager ref={companyManagerRef} />
        )}
        
        {activeTab === 'children' && (
          <ChildrenManager ref={childrenManagerRef} />
        )}
      </div>
    </div>
  )
}

export default AdminPortal 