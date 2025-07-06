import React, { useState, useEffect } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import { relationshipService } from '../services/relationshipService'
import type { 
  ParentChildRelationship, 
  ParentChildRelationshipCreate, 
  UserRelationships
} from '../models'
import { RelationshipType } from '../models'

interface RelationshipManagerProps {
  userId?: string
}

const RelationshipManager: React.FC<RelationshipManagerProps> = ({ userId }) => {
  const { t } = useLanguage()
  const [relationships, setRelationships] = useState<UserRelationships | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newRelationship, setNewRelationship] = useState<ParentChildRelationshipCreate>({
    parent_id: '',
    child_id: '',
    relationship_type: RelationshipType.PARENT,
    notes: ''
  })

  useEffect(() => {
    if (userId) {
      loadUserRelationships(userId)
    }
  }, [userId])

  const loadUserRelationships = async (userId: string) => {
    setLoading(true)
    setError(null)
    try {
      const data = await relationshipService.getUserRelationships(userId)
      setRelationships(data)
    } catch (err) {
      setError(t('relationships.loadError'))
    } finally {
      setLoading(false)
    }
  }

  const handleCreateRelationship = async () => {
    if (!newRelationship.parent_id || !newRelationship.child_id) {
      setError(t('relationships.parentRequired'))
      return
    }

    setLoading(true)
    setError(null)
    try {
      await relationshipService.createRelationship(newRelationship)
      setNewRelationship({
        parent_id: '',
        child_id: '',
        relationship_type: RelationshipType.PARENT,
        notes: ''
      })
      setShowCreateForm(false)
      if (userId) {
        await loadUserRelationships(userId)
      }
    } catch (err) {
      setError(t('relationships.createError'))
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteRelationship = async (relationshipId: string) => {
    if (!confirm(t('relationships.deleteConfirm'))) {
      return
    }

    setLoading(true)
    setError(null)
    try {
      await relationshipService.deleteRelationship(relationshipId)
      if (userId) {
        await loadUserRelationships(userId)
      }
    } catch (err) {
      setError(t('relationships.deleteError'))
    } finally {
      setLoading(false)
    }
  }

  const renderRelationshipCard = (relationship: ParentChildRelationship, type: string) => (
    <div key={relationship.id} className="relationship-card">
      <div className="relationship-header">
        <h4>{type} {t('relationships.title')}</h4>
        <span className={`status-badge ${relationship.is_active ? 'active' : 'inactive'}`}>
          {relationship.is_active ? t('relationships.active') : t('relationships.inactive')}
        </span>
      </div>
      <div className="relationship-details">
        <p><strong>{t('relationships.parentId')}:</strong> {relationship.parent_id}</p>
        <p><strong>{t('relationships.childId')}:</strong> {relationship.child_id}</p>
        {relationship.escort_id && (
          <p><strong>{t('relationships.escortId')}:</strong> {relationship.escort_id}</p>
        )}
        {relationship.notes && (
          <p><strong>{t('relationships.notes')}:</strong> {relationship.notes}</p>
        )}
        <p><strong>{t('relationships.created')}:</strong> {new Date(relationship.created_at).toLocaleDateString()}</p>
      </div>
      <div className="relationship-actions">
        <button 
          className="btn-small btn-danger"
          onClick={() => handleDeleteRelationship(relationship.id)}
          disabled={loading}
        >
          {t('common.delete')}
        </button>
      </div>
    </div>
  )

  if (loading && !relationships) {
    return <div className="loading">{t('common.loading')}</div>
  }

  if (error) {
    return <div className="error-message">{t('common.error')}: {error}</div>
  }

  return (
    <div className="relationship-manager">
      <div className="section-header">
        <h2>{t('relationships.title')}</h2>
        <button 
          className="btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? t('common.cancel') : t('relationships.createRelationship')}
        </button>
      </div>

      {showCreateForm && (
        <div className="create-relationship-form">
          <h3>{t('relationships.createNewRelationship')}</h3>
          <div className="form-group">
            <label>{t('relationships.parentId')}:</label>
            <input
              type="text"
              value={newRelationship.parent_id}
              onChange={(e) => setNewRelationship(prev => ({ ...prev, parent_id: e.target.value }))}
              placeholder={t('relationships.enterParentId')}
            />
          </div>
          <div className="form-group">
            <label>{t('relationships.childId')}:</label>
            <input
              type="text"
              value={newRelationship.child_id}
              onChange={(e) => setNewRelationship(prev => ({ ...prev, child_id: e.target.value }))}
              placeholder={t('relationships.enterChildId')}
            />
          </div>
          <div className="form-group">
            <label>{t('relationships.relationshipType')}:</label>
            <select
              value={newRelationship.relationship_type}
              onChange={(e) => setNewRelationship(prev => ({ 
                ...prev, 
                relationship_type: e.target.value as RelationshipType 
              }))}
            >
              <option value={RelationshipType.PARENT}>{t('relationships.parent')}</option>
              <option value={RelationshipType.CHILD}>{t('relationships.child')}</option>
              <option value={RelationshipType.ESCORT}>{t('relationships.escort')}</option>
            </select>
          </div>
          <div className="form-group">
            <label>{t('relationships.notes')}:</label>
            <textarea
              value={newRelationship.notes || ''}
              onChange={(e) => setNewRelationship(prev => ({ ...prev, notes: e.target.value }))}
              placeholder={t('relationships.optionalNotes')}
            />
          </div>
          <div className="form-actions">
            <button 
              className="btn-primary"
              onClick={handleCreateRelationship}
              disabled={loading}
            >
              {t('relationships.createRelationship')}
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

      {relationships && (
        <div className="relationships-sections">
          {relationships.as_parent.length > 0 && (
            <div className="relationships-section">
              <h3>{t('relationships.asParent')} ({relationships.as_parent.length})</h3>
              <div className="relationships-grid">
                {relationships.as_parent.map(rel => renderRelationshipCard(rel, t('relationships.parent')))}
              </div>
            </div>
          )}

          {relationships.as_child.length > 0 && (
            <div className="relationships-section">
              <h3>{t('relationships.asChild')} ({relationships.as_child.length})</h3>
              <div className="relationships-grid">
                {relationships.as_child.map(rel => renderRelationshipCard(rel, t('relationships.child')))}
              </div>
            </div>
          )}

          {relationships.as_escort.length > 0 && (
            <div className="relationships-section">
              <h3>{t('relationships.asEscort')} ({relationships.as_escort.length})</h3>
              <div className="relationships-grid">
                {relationships.as_escort.map(rel => renderRelationshipCard(rel, t('relationships.escort')))}
              </div>
            </div>
          )}

          {relationships.as_parent.length === 0 && 
           relationships.as_child.length === 0 && 
           relationships.as_escort.length === 0 && (
            <div className="no-relationships">
              <p>{t('relationships.noRelationships')}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default RelationshipManager 