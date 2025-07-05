import { Ride } from './ride'
import { UserPreferences } from './user_preferences'

/**
 * User interface for user management
 */
export interface User {
  id: string
  email: string
  password: string
  name: string
  phone?: string
  profilePicture?: string | null
  createdAt: string
  updatedAt: string
  rideHistory: Ride[]
  preferences: UserPreferences
  // Authentication field
  token?: string
  // Relationship fields
  parent_ids?: string[]
  child_ids?: string[]
  escort_ids?: string[]
  is_child?: boolean
  is_parent?: boolean
  is_escort?: boolean
} 