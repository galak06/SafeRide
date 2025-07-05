import React, { useState, useEffect } from 'react'
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
      setError(err instanceof Error ? err.message : 'Failed to load relationships')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateRelationship = async () => {
    if (!newRelationship.parent_id || !newRelationship.child_id) {
      setError('Parent and Child IDs are required')
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
      setError(err instanceof Error ? err.message : 'Failed to create relationship')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteRelationship = async (relationshipId: string) => {
    if (!confirm('Are you sure you want to delete this relationship?')) {
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
      setError(err instanceof Error ? err.message : 'Failed to delete relationship')
    } finally {
      setLoading(false)
    }
  }

  const renderRelationshipCard = (relationship: ParentChildRelationship, type: string) => (
    <div key={relationship.id} className="relationship-card">
      <div className="relationship-header">
        <h4>{type} Relationship</h4>
        <span className={`status-badge ${relationship.is_active ? 'active' : 'inactive'}`}>
          {relationship.is_active ? 'Active' : 'Inactive'}
        </span>
      </div>
      <div className="relationship-details">
        <p><strong>Parent ID:</strong> {relationship.parent_id}</p>
        <p><strong>Child ID:</strong> {relationship.child_id}</p>
        {relationship.escort_id && (
          <p><strong>Escort ID:</strong> {relationship.escort_id}</p>
        )}
        {relationship.notes && (
          <p><strong>Notes:</strong> {relationship.notes}</p>
        )}
        <p><strong>Created:</strong> {new Date(relationship.created_at).toLocaleDateString()}</p>
      </div>
      <div className="relationship-actions">
        <button 
          className="btn-small btn-danger"
          onClick={() => handleDeleteRelationship(relationship.id)}
          disabled={loading}
        >
          Delete
        </button>
      </div>
    </div>
  )

  if (loading && !relationships) {
    return <div className="loading">Loading relationships...</div>
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>
  }

  return (
    <div className="relationship-manager">
      <div className="section-header">
        <h2>Parent-Child Relationships</h2>
        <button 
          className="btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Cancel' : 'Create Relationship'}
        </button>
      </div>

      {showCreateForm && (
        <div className="create-relationship-form">
          <h3>Create New Relationship</h3>
          <div className="form-group">
            <label>Parent ID:</label>
            <input
              type="text"
              value={newRelationship.parent_id}
              onChange={(e) => setNewRelationship(prev => ({ ...prev, parent_id: e.target.value }))}
              placeholder="Enter parent user ID"
            />
          </div>
          <div className="form-group">
            <label>Child ID:</label>
            <input
              type="text"
              value={newRelationship.child_id}
              onChange={(e) => setNewRelationship(prev => ({ ...prev, child_id: e.target.value }))}
              placeholder="Enter child user ID"
            />
          </div>
          <div className="form-group">
            <label>Relationship Type:</label>
            <select
              value={newRelationship.relationship_type}
              onChange={(e) => setNewRelationship(prev => ({ 
                ...prev, 
                relationship_type: e.target.value as RelationshipType 
              }))}
            >
              <option value={RelationshipType.PARENT}>Parent</option>
              <option value={RelationshipType.CHILD}>Child</option>
              <option value={RelationshipType.ESCORT}>Escort</option>
            </select>
          </div>
          <div className="form-group">
            <label>Notes:</label>
            <textarea
              value={newRelationship.notes || ''}
              onChange={(e) => setNewRelationship(prev => ({ ...prev, notes: e.target.value }))}
              placeholder="Optional notes about the relationship"
            />
          </div>
          <div className="form-actions">
            <button 
              className="btn-primary"
              onClick={handleCreateRelationship}
              disabled={loading}
            >
              Create Relationship
            </button>
            <button 
              className="btn-secondary"
              onClick={() => setShowCreateForm(false)}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {relationships && (
        <div className="relationships-sections">
          {relationships.as_parent.length > 0 && (
            <div className="relationships-section">
              <h3>As Parent ({relationships.as_parent.length})</h3>
              <div className="relationships-grid">
                {relationships.as_parent.map(rel => renderRelationshipCard(rel, 'Parent'))}
              </div>
            </div>
          )}

          {relationships.as_child.length > 0 && (
            <div className="relationships-section">
              <h3>As Child ({relationships.as_child.length})</h3>
              <div className="relationships-grid">
                {relationships.as_child.map(rel => renderRelationshipCard(rel, 'Child'))}
              </div>
            </div>
          )}

          {relationships.as_escort.length > 0 && (
            <div className="relationships-section">
              <h3>As Escort ({relationships.as_escort.length})</h3>
              <div className="relationships-grid">
                {relationships.as_escort.map(rel => renderRelationshipCard(rel, 'Escort'))}
              </div>
            </div>
          )}

          {relationships.as_parent.length === 0 && 
           relationships.as_child.length === 0 && 
           relationships.as_escort.length === 0 && (
            <div className="no-relationships">
              <p>No relationships found for this user.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default RelationshipManager 