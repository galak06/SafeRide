import React, { useState, useEffect } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import { childService } from '../services/childService'
import type { Child, ChildCreate, User } from '../models'

const ChildrenManager: React.FC = () => {
  const { t } = useLanguage()
  const [children, setChildren] = useState<Child[]>([])
  const [parents, setParents] = useState<User[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newChild, setNewChild] = useState<ChildCreate>({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    parent_id: '',
    date_of_birth: '',
    grade: '',
    school: '',
    emergency_contact: '',
    notes: ''
  })

  useEffect(() => {
    loadChildren()
    loadParents()
  }, [])

  const loadChildren = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await childService.getAllChildren()
      console.log('Loaded children:', data) // Debug log
      setChildren(data)
    } catch (err) {
      console.error('Failed to load children:', err) // Debug log
      setError(t('children.loadError'))
      setChildren([]) // Clear children on error
    } finally {
      setLoading(false)
    }
  }

  const loadParents = async () => {
    try {
      // For now, we'll use mock data - implement actual API call later
      const mockParents: User[] = [
        {
          id: 'admin-001',
          email: 'admin@saferide.com',
          name: 'Admin User',
          password: 'hashed_password',
          phone: '+1234567890',
          profilePicture: null,
          createdAt: '2025-07-05T11:36:53.781381+03:00',
          updatedAt: '2025-07-05T22:09:32.448759+03:00',
          rideHistory: [],
          preferences: {
            defaultPaymentMethod: 'card',
            notifications: true,
            language: 'en'
          },
          is_parent: true
        }
      ]
      setParents(mockParents)
    } catch (err) {
      console.error('Failed to load parents:', err)
    }
  }

  const handleCreateChild = async () => {
    if (!newChild.first_name || !newChild.last_name || !newChild.parent_id) {
      setError(t('children.createError'))
      return
    }

    setLoading(true)
    setError(null)
    try {
      const createdChild = await childService.createChild(newChild)
      setChildren(prev => [...prev, createdChild])
      setNewChild({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        parent_id: '',
        date_of_birth: '',
        grade: '',
        school: '',
        emergency_contact: '',
        notes: ''
      })
      setShowCreateForm(false)
    } catch (err) {
      setError(t('children.createError'))
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteChild = async (childId: string) => {
    if (!confirm(t('children.deleteConfirm'))) {
      return
    }

    setLoading(true)
    setError(null)
    try {
      await childService.deleteChild(childId)
      setChildren(prev => prev.filter(child => child.id !== childId))
    } catch (err) {
      setError(t('children.deleteError'))
    } finally {
      setLoading(false)
    }
  }

  const getParentName = (parentId: string) => {
    const parent = parents.find(p => p.id === parentId)
    return parent ? parent.name : t('children.unknownParent')
  }

  const renderChildCard = (child: Child) => (
    <div key={child.id} className="child-card">
      <div className="child-header">
        <h4>{child.first_name} {child.last_name}</h4>
        <span className={`status-badge ${child.is_active ? 'active' : 'inactive'}`}>
          {child.is_active ? t('relationships.active') : t('relationships.inactive')}
        </span>
      </div>
      <div className="child-details">
        <p><strong>{t('children.parent')}:</strong> {getParentName(child.parent_id)}</p>
        <p><strong>{t('auth.email')}:</strong> {child.email || t('children.notProvided')}</p>
        <p><strong>{t('children.phone')}:</strong> {child.phone || t('children.notProvided')}</p>
        <p><strong>{t('children.dateOfBirth')}:</strong> {child.date_of_birth ? new Date(child.date_of_birth).toLocaleDateString() : t('children.notProvided')}</p>
        <p><strong>{t('children.grade')}:</strong> {child.grade || t('children.notProvided')}</p>
        <p><strong>{t('children.school')}:</strong> {child.school || t('children.notProvided')}</p>
        <p><strong>{t('children.emergencyContact')}:</strong> {child.emergency_contact || t('children.notProvided')}</p>
        {child.notes && (
          <p><strong>{t('relationships.notes')}:</strong> {child.notes}</p>
        )}
        <p><strong>{t('children.added')}:</strong> {new Date(child.created_at).toLocaleDateString()}</p>
      </div>
      <div className="child-actions">
        <button 
          className="btn-small btn-danger"
          onClick={() => handleDeleteChild(child.id)}
          disabled={loading}
        >
          {t('common.delete')}
        </button>
      </div>
    </div>
  )

  if (loading && children.length === 0) {
    return <div className="loading">{t('common.loading')}</div>
  }

  if (error) {
    return <div className="error-message">{t('common.error')}: {error}</div>
  }

  return (
    <div className="children-manager">
      <div className="section-header">
        <h2>{t('children.title')}</h2>
        <button 
          className="btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? t('common.cancel') : t('children.addChild')}
        </button>
      </div>

      {showCreateForm && (
        <div className="create-child-form">
          <h3>{t('children.createChild')}</h3>
          <div className="form-row">
            <div className="form-group">
              <label>{t('children.firstName')} *:</label>
              <input
                type="text"
                value={newChild.first_name}
                onChange={(e) => setNewChild(prev => ({ ...prev, first_name: e.target.value }))}
                placeholder={t('children.enterFirstName')}
                required
              />
            </div>
            <div className="form-group">
              <label>{t('children.lastName')} *:</label>
              <input
                type="text"
                value={newChild.last_name}
                onChange={(e) => setNewChild(prev => ({ ...prev, last_name: e.target.value }))}
                placeholder={t('children.enterLastName')}
                required
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>{t('auth.email')}:</label>
              <input
                type="email"
                value={newChild.email}
                onChange={(e) => setNewChild(prev => ({ ...prev, email: e.target.value }))}
                placeholder={t('auth.email')}
              />
            </div>
            <div className="form-group">
              <label>{t('children.phone')}:</label>
              <input
                type="tel"
                value={newChild.phone}
                onChange={(e) => setNewChild(prev => ({ ...prev, phone: e.target.value }))}
                placeholder={t('children.enterPhone')}
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>{t('children.dateOfBirth')}:</label>
              <input
                type="date"
                value={newChild.date_of_birth}
                onChange={(e) => setNewChild(prev => ({ ...prev, date_of_birth: e.target.value }))}
              />
            </div>
            <div className="form-group">
              <label>{t('children.grade')}:</label>
              <input
                type="text"
                value={newChild.grade}
                onChange={(e) => setNewChild(prev => ({ ...prev, grade: e.target.value }))}
                placeholder={t('children.enterGrade')}
              />
            </div>
          </div>
          <div className="form-group">
            <label>{t('children.school')}:</label>
            <input
              type="text"
              value={newChild.school}
              onChange={(e) => setNewChild(prev => ({ ...prev, school: e.target.value }))}
              placeholder={t('children.enterSchool')}
            />
          </div>
          <div className="form-group">
            <label>{t('children.emergencyContact')}:</label>
            <input
              type="text"
              value={newChild.emergency_contact}
              onChange={(e) => setNewChild(prev => ({ ...prev, emergency_contact: e.target.value }))}
              placeholder={t('children.enterEmergencyContact')}
            />
          </div>
          <div className="form-group">
            <label>{t('relationships.notes')}:</label>
            <textarea
              value={newChild.notes}
              onChange={(e) => setNewChild(prev => ({ ...prev, notes: e.target.value }))}
              placeholder={t('children.enterNotes')}
              rows={3}
            />
          </div>
          <div className="form-group">
            <label>{t('children.parentId')} *:</label>
            <select
              value={newChild.parent_id}
              onChange={(e) => setNewChild(prev => ({ ...prev, parent_id: e.target.value }))}
              required
            >
              <option value="">{t('children.selectParent')}</option>
              {parents.map(parent => (
                <option key={parent.id} value={parent.id}>
                  {parent.name} ({parent.email})
                </option>
              ))}
            </select>
          </div>
          <div className="form-actions">
            <button 
              className="btn-primary"
              onClick={handleCreateChild}
              disabled={loading}
            >
              {t('children.createChild')}
            </button>
            <button 
              className="btn-secondary"
              onClick={() => setShowCreateForm(false)}
              disabled={loading}
            >
              {t('common.cancel')}
            </button>
          </div>
        </div>
      )}

      <div className="children-section">
        <h3>{t('children.title')}</h3>
        {children.length > 0 ? (
          <div className="children-grid">
            {children.map(renderChildCard)}
          </div>
        ) : (
          <div className="no-children">
            <p>{t('children.noChildren')}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default ChildrenManager 