import { User } from '../interfaces/user'

/**
 * Authentication response interface
 */
export interface AuthResponse {
  success: boolean
  message: string
  user?: Omit<User, 'password'>
  token?: string
} 