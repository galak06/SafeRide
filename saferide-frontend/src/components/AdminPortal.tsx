import React, { useState } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import ChildrenManager from './ChildrenManager'
import RelationshipManager from './RelationshipManager'
import CompanyManager from './CompanyManager'
import './AdminPortal.css'

interface AdminPortalProps {}

const AdminPortal: React.FC<AdminPortalProps> = () => {
  const { t } = useLanguage()
  const [activeTab, setActiveTab] = useState<'dashboard' | 'drivers' | 'companies' | 'relationships' | 'children'>('dashboard')

  return (
    <div className="admin-portal">
      <div className="admin-header">
        <h1>{t('admin.portal')}</h1>
        <p>{t('admin.manageDrivers')}</p>
      </div>
      
      <div className="admin-tabs">
        <button
          className={`tab-button ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          {t('admin.dashboard')}
        </button>
        <button
          className={`tab-button ${activeTab === 'drivers' ? 'active' : ''}`}
          onClick={() => setActiveTab('drivers')}
        >
          {t('admin.drivers')}
        </button>
        <button
          className={`tab-button ${activeTab === 'companies' ? 'active' : ''}`}
          onClick={() => setActiveTab('companies')}
        >
          {t('admin.companies')}
        </button>
        <button
          className={`tab-button ${activeTab === 'relationships' ? 'active' : ''}`}
          onClick={() => setActiveTab('relationships')}
        >
          {t('admin.relationships')}
        </button>
        <button
          className={`tab-button ${activeTab === 'children' ? 'active' : ''}`}
          onClick={() => setActiveTab('children')}
        >
          {t('admin.children')}
        </button>
      </div>
      
      <div className="admin-content">
        {activeTab === 'dashboard' && (
          <div className="dashboard">
            <h2>{t('admin.systemDashboard')}</h2>
            <div className="dashboard-stats">
              <div className="stat-card">
                <h3>{t('admin.totalDrivers')}</h3>
                <div className="stat-number">0</div>
                <p>{t('admin.activeDrivers')}</p>
              </div>
              <div className="stat-card">
                <h3>{t('admin.totalCompanies')}</h3>
                <div className="stat-number">0</div>
                <p>{t('admin.registeredCompanies')}</p>
              </div>
              <div className="stat-card">
                <h3>{t('admin.totalChildren')}</h3>
                <div className="stat-number">0</div>
                <p>{t('admin.childrenInSystem')}</p>
              </div>
              <div className="stat-card">
                <h3>{t('admin.activeRides')}</h3>
                <div className="stat-number">0</div>
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
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'drivers' && (
          <div className="drivers-placeholder">
            <h2>{t('drivers.title')}</h2>
            <p>{t('drivers.description')}</p>
            <p>{t('drivers.features')}</p>
            <ul>
              <li>{t('drivers.addDrivers')}</li>
              <li>{t('drivers.createCompanies')}</li>
              <li>{t('drivers.assignDrivers')}</li>
              <li>{t('drivers.viewStats')}</li>
              <li>{t('drivers.manageSettings')}</li>
            </ul>
          </div>
        )}
        
        {activeTab === 'companies' && (
          <CompanyManager />
        )}
        
        {activeTab === 'relationships' && (
          <RelationshipManager userId="admin-001" />
        )}
        
        {activeTab === 'children' && (
          <ChildrenManager />
        )}
      </div>
    </div>
  )
}

export default AdminPortal 