import type { 
  ParentChildRelationship, 
  ParentChildRelationshipCreate, 
  ParentChildRelationshipUpdate, 
  UserRelationships 
} from '../models'

/**
 * Service for managing parent-child relationships
 * Follows SOLID principles and provides comprehensive relationship management
 */
class RelationshipService {
  private baseUrl: string = 'http://localhost:8000'

  /**
   * Create a new parent-child relationship
   */
  async createRelationship(relationship: ParentChildRelationshipCreate): Promise<ParentChildRelationship> {
    const response = await fetch(`${this.baseUrl}/api/relationships`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(relationship),
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Failed to create relationship: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Get all relationships for a specific user
   */
  async getUserRelationships(userId: string): Promise<UserRelationships> {
    const response = await fetch(`${this.baseUrl}/api/users/${userId}/relationships`, {
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Failed to get user relationships: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Get all relationships where user is a parent
   */
  async getParentRelationships(userId: string): Promise<ParentChildRelationship[]> {
    const response = await fetch(`${this.baseUrl}/api/users/${userId}/relationships/parent`, {
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Failed to get parent relationships: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Get all relationships where user is a child
   */
  async getChildRelationships(userId: string): Promise<ParentChildRelationship[]> {
    const response = await fetch(`${this.baseUrl}/api/users/${userId}/relationships/child`, {
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Failed to get child relationships: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Get all relationships where user is an escort
   */
  async getEscortRelationships(userId: string): Promise<ParentChildRelationship[]> {
    const response = await fetch(`${this.baseUrl}/api/users/${userId}/relationships/escort`, {
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Failed to get escort relationships: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Update an existing relationship
   */
  async updateRelationship(
    relationshipId: string, 
    updates: ParentChildRelationshipUpdate
  ): Promise<ParentChildRelationship> {
    const response = await fetch(`${this.baseUrl}/api/relationships/${relationshipId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates),
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Failed to update relationship: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Delete a relationship
   */
  async deleteRelationship(relationshipId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/api/relationships/${relationshipId}`, {
      method: 'DELETE',
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Failed to delete relationship: ${response.statusText}`)
    }
  }

  /**
   * Assign an escort to a relationship
   */
  async assignEscort(relationshipId: string, escortId: string): Promise<ParentChildRelationship> {
    return this.updateRelationship(relationshipId, { escort_id: escortId })
  }

  /**
   * Remove escort from a relationship
   */
  async removeEscort(relationshipId: string): Promise<ParentChildRelationship> {
    return this.updateRelationship(relationshipId, { escort_id: undefined })
  }

  /**
   * Get all children for a parent
   */
  async getChildrenForParent(parentId: string): Promise<ParentChildRelationship[]> {
    return this.getParentRelationships(parentId)
  }

  /**
   * Get all parents for a child
   */
  async getParentsForChild(childId: string): Promise<ParentChildRelationship[]> {
    return this.getChildRelationships(childId)
  }

  /**
   * Get all children being escorted by an escort
   */
  async getChildrenForEscort(escortId: string): Promise<ParentChildRelationship[]> {
    return this.getEscortRelationships(escortId)
  }
}

// Export singleton instance
export const relationshipService = new RelationshipService() 