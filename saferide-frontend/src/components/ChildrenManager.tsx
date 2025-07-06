import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import { childService } from '../services/childService'
import type { Child, ChildCreate, User } from '../models'

export interface ChildrenManagerRef {
  closeForm: () => void;
}

const ChildrenManager = forwardRef<ChildrenManagerRef>((props, ref) => {
  const { t } = useLanguage()
  const [children, setChildren] = useState<Child[]>([])
  const [parents, setParents] = useState<User[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const defaultChildData: ChildCreate = {
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
  };

  // Atomic state for form and visibility
  interface ChildrenFormState {
    showCreateForm: boolean;
    newChild: ChildCreate;
  }

  const getInitialChildrenFormState = (): ChildrenFormState => {
    const savedShowForm = localStorage.getItem('childrenShowCreateForm');
    const savedChildData = localStorage.getItem('childrenFormData');
    if (savedShowForm === 'true') {
      if (savedChildData) {
        try {
          return {
            showCreateForm: true,
            newChild: JSON.parse(savedChildData)
          };
        } catch (e) {
          console.warn('Failed to parse saved child form data:', e);
        }
      }
      return { showCreateForm: true, newChild: { ...defaultChildData } };
    }
    return { showCreateForm: false, newChild: { ...defaultChildData } };
  };

  const [childrenFormState, setChildrenFormState] = useState<ChildrenFormState>(getInitialChildrenFormState);
  const { showCreateForm, newChild } = childrenFormState;

  // Add edit mode state
  const [editChildId, setEditChildId] = useState<string | null>(null);

  // Expose closeForm method to parent component
  useImperativeHandle(ref, () => ({
    closeForm: () => {
      setChildrenFormState({ showCreateForm: false, newChild: { ...defaultChildData } });
    }
  }));

  // Save to localStorage whenever state changes
  useEffect(() => {
    localStorage.setItem('childrenShowCreateForm', JSON.stringify(showCreateForm));
    localStorage.setItem('childrenFormData', JSON.stringify(newChild));
  }, [showCreateForm, newChild]);

  // When clicking Add New Child, clear form and localStorage
  const handleShowCreateForm = () => {
    if (!showCreateForm) {
      setChildrenFormState({ showCreateForm: true, newChild: { ...defaultChildData } });
    } else {
      setChildrenFormState({ showCreateForm: false, newChild: { ...defaultChildData } });
    }
  };

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
      
      // Reset form and clear localStorage
      setChildrenFormState({ showCreateForm: false, newChild: { ...defaultChildData } });
    } catch (err) {
      setError(t('children.createError'))
    } finally {
      setLoading(false)
    }
  }

  // Update form data
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setChildrenFormState(prev => ({
      ...prev,
      newChild: {
        ...prev.newChild,
        [name]: value
      }
    }));
  };

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

  // When clicking Edit, populate form and switch to edit mode
  const handleEditChild = (child: Child) => {
    setChildrenFormState({ showCreateForm: true, newChild: { ...child } });
    setEditChildId(child.id);
    // Scroll to top to show the form
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Cancel edit
  const handleCancelEdit = () => {
    setChildrenFormState({ showCreateForm: false, newChild: { ...defaultChildData } });
    setEditChildId(null);
  };

  // Update form submission logic
  const handleCreateOrUpdateChild = async () => {
    if (!newChild.first_name || !newChild.last_name || !newChild.parent_id) {
      setError(t('children.createError'));
      return;
    }
    setLoading(true);
    setError(null);
    try {
      if (editChildId) {
        await childService.updateChild(editChildId, newChild);
      } else {
        const createdChild = await childService.createChild(newChild);
        setChildren(prev => [...prev, createdChild]);
      }
      setChildrenFormState({ showCreateForm: false, newChild: { ...defaultChildData } });
      setEditChildId(null);
      await loadChildren();
    } catch (err) {
      setError(t('children.createError'));
    } finally {
      setLoading(false);
    }
  };

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
        <button 
          className="btn-small btn-primary"
          onClick={() => handleEditChild(child)}
          disabled={loading}
        >
          Edit
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
          onClick={handleShowCreateForm}
        >
          {showCreateForm ? t('common.cancel') : t('children.addChild')}
        </button>
      </div>

      {showCreateForm && (
        <form onSubmit={e => { e.preventDefault(); handleCreateOrUpdateChild(); }} className="create-child-form">
          <h3>{editChildId ? `Edit ${newChild.first_name} ${newChild.last_name}` : t('children.addTitle')}</h3>
          <div className="form-row">
            <div className="form-group">
              <label>{t('children.firstName')} *:</label>
              <input
                type="text"
                name="first_name"
                value={newChild.first_name}
                onChange={handleInputChange}
                placeholder={t('children.enterFirstName')}
                required
              />
            </div>
            <div className="form-group">
              <label>{t('children.lastName')} *:</label>
              <input
                type="text"
                name="last_name"
                value={newChild.last_name}
                onChange={handleInputChange}
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
                name="email"
                value={newChild.email}
                onChange={handleInputChange}
                placeholder={t('auth.email')}
              />
            </div>
            <div className="form-group">
              <label>{t('children.phone')}:</label>
              <input
                type="tel"
                name="phone"
                value={newChild.phone}
                onChange={handleInputChange}
                placeholder={t('children.enterPhone')}
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>{t('children.dateOfBirth')}:</label>
              <input
                type="date"
                name="date_of_birth"
                value={newChild.date_of_birth}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label>{t('children.grade')}:</label>
              <input
                type="text"
                name="grade"
                value={newChild.grade}
                onChange={handleInputChange}
                placeholder={t('children.enterGrade')}
              />
            </div>
          </div>
          <div className="form-group">
            <label>{t('children.school')}:</label>
            <input
              type="text"
              name="school"
              value={newChild.school}
              onChange={handleInputChange}
              placeholder={t('children.enterSchool')}
            />
          </div>
          <div className="form-group">
            <label>{t('children.emergencyContact')}:</label>
            <input
              type="text"
              name="emergency_contact"
              value={newChild.emergency_contact}
              onChange={handleInputChange}
              placeholder={t('children.enterEmergencyContact')}
            />
          </div>
          <div className="form-group">
            <label>{t('relationships.notes')}:</label>
            <textarea
              name="notes"
              value={newChild.notes}
              onChange={handleInputChange}
              placeholder={t('children.enterNotes')}
              rows={3}
            />
          </div>
          <div className="form-group">
            <label>{t('children.parentId')} *:</label>
            <select
              name="parent_id"
              value={newChild.parent_id}
              onChange={handleInputChange}
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
              type="submit"
              disabled={loading}
            >
              {editChildId ? 'Save' : t('children.add')}
            </button>
            {editChildId && <button 
              className="btn-secondary"
              type="button"
              onClick={handleCancelEdit}
              disabled={loading}
            >
              {t('children.cancelEdit')}
            </button>}
            <button 
              className="btn-secondary"
              onClick={handleShowCreateForm}
              disabled={loading}
            >
              {t('common.cancel')}
            </button>
          </div>
        </form>
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
})

export default ChildrenManager 