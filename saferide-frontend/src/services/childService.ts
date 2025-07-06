import type { Child, ChildCreate, ChildUpdate } from '../models'
import { apiService } from './apiService'

/**
 * Service for managing children in the system
 * Follows SOLID principles and provides comprehensive child management
 */
class ChildService {
  /**
   * Get all children in the system
   */
  async getAllChildren(): Promise<Child[]> {
    return apiService.request<Child[]>('/api/children')
  }

  /**
   * Get a specific child by ID
   */
  async getChildById(childId: string): Promise<Child> {
    return apiService.request<Child>(`/api/children/${childId}`)
  }

  /**
   * Get all children for a specific parent
   */
  async getChildrenByParent(parentId: string): Promise<Child[]> {
    return apiService.request<Child[]>(`/api/children/parent/${parentId}`)
  }

  /**
   * Create a new child
   */
  async createChild(childData: ChildCreate): Promise<Child> {
    return apiService.request<Child>('/api/children', {
      method: 'POST',
      body: JSON.stringify(childData),
    })
  }

  /**
   * Update an existing child
   */
  async updateChild(childId: string, childData: ChildUpdate): Promise<Child> {
    return apiService.request<Child>(`/api/children/${childId}`, {
      method: 'PUT',
      body: JSON.stringify(childData),
    })
  }

  /**
   * Delete a child (soft delete)
   */
  async deleteChild(childId: string): Promise<void> {
    await apiService.request<void>(`/api/children/${childId}`, {
      method: 'DELETE',
    })
  }

  /**
   * Search children by name or email
   */
  async searchChildren(searchTerm: string): Promise<Child[]> {
    return apiService.request<Child[]>(`/api/children/search/?q=${encodeURIComponent(searchTerm)}`)
  }
}

// Export singleton instance
export const childService = new ChildService() 