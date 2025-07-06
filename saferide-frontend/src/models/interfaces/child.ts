/**
 * Child interface for children management
 */
export interface Child {
  id: string
  first_name: string
  last_name: string
  email?: string
  phone?: string
  parent_id: string
  date_of_birth?: string
  grade?: string
  school?: string
  emergency_contact?: string
  notes?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

/**
 * Create child request interface
 */
export interface ChildCreate {
  first_name: string
  last_name: string
  email?: string
  phone?: string
  parent_id: string
  date_of_birth?: string
  grade?: string
  school?: string
  emergency_contact?: string
  notes?: string
}

/**
 * Update child request interface
 */
export interface ChildUpdate {
  first_name?: string
  last_name?: string
  email?: string
  phone?: string
  parent_id?: string
  date_of_birth?: string
  grade?: string
  school?: string
  emergency_contact?: string
  notes?: string
  is_active?: boolean
} 